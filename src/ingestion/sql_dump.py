from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any


@dataclass
class TableSchema:
    table_name: str
    columns: list[str]


@dataclass
class ParsedTable:
    schema: TableSchema
    rows: list[dict[str, Any]]


class SQLDumpParser:
    """
    Lightweight MySQL/MariaDB dump parser.

    Does NOT execute SQL.

    Supports:
    - CREATE TABLE
    - INSERT INTO ... VALUES
    - NULL
    - integers
    - decimals
    - quoted strings
    - escaped quotes
    - semicolons inside quoted strings
    - commas inside quoted strings
    - parentheses inside quoted strings
    """

    CREATE_TABLE_RE = re.compile(
        r"CREATE\s+TABLE\s+`(?P<table>[^`]+)`\s*\((?P<body>.*?)\)"
        r"\s*ENGINE=",
        re.IGNORECASE | re.DOTALL,
    )

    INSERT_START_RE = re.compile(
        r"INSERT\s+INTO\s+`(?P<table>[^`]+)`"
        r"\s*(?:\((?P<columns>.*?)\))?"
        r"\s*VALUES\s*",
        re.IGNORECASE | re.DOTALL,
    )

    COLUMN_RE = re.compile(
        r"^\s*`(?P<name>[^`]+)`\s+",
        re.MULTILINE,
    )

    def parse_file(self, path: Path) -> ParsedTable:
        sql = path.read_text(
            encoding="utf-8"
        )

        schemas = self._parse_schemas(sql)
        inserts = self._extract_insert_statements(sql)

        if not inserts:
            raise ValueError(
                f"No INSERT statements found in {path}"
            )

        table_names = {
            insert["table"]
            for insert in inserts
        }

        if len(table_names) != 1:
            raise ValueError(
                f"Expected one table in {path}, "
                f"found: {sorted(table_names)}"
            )

        table_name = next(iter(table_names))

        if table_name not in schemas:
            raise ValueError(
                f"INSERT table '{table_name}' has no "
                f"matching CREATE TABLE schema"
            )

        schema = schemas[table_name]

        rows: list[dict[str, Any]] = []

        for insert in inserts:

            explicit_columns = insert["columns"]

            if explicit_columns:
                columns = self._parse_identifier_list(
                    explicit_columns
                )
            else:
                columns = schema.columns

            value_block = insert["values"]

            tuples = self._parse_value_tuples(
                value_block
            )

            for values in tuples:

                if len(values) != len(columns):
                    raise ValueError(
                        f"Column/value mismatch in table "
                        f"'{table_name}': "
                        f"{len(columns)} columns vs "
                        f"{len(values)} values"
                    )

                rows.append(
                    dict(
                        zip(columns, values)
                    )
                )

        return ParsedTable(
            schema=schema,
            rows=rows,
        )

    # ============================================================
    # CREATE TABLE
    # ============================================================

    def _parse_schemas(
        self,
        sql: str,
    ) -> dict[str, TableSchema]:

        schemas: dict[str, TableSchema] = {}

        for match in self.CREATE_TABLE_RE.finditer(sql):

            table_name = match.group("table")
            body = match.group("body")

            columns: list[str] = []

            for line in body.splitlines():

                line = line.strip()

                if not line.startswith("`"):
                    continue

                column_match = self.COLUMN_RE.match(line)

                if column_match:
                    columns.append(
                        column_match.group("name")
                    )

            if not columns:
                raise ValueError(
                    f"No columns found for table "
                    f"'{table_name}'"
                )

            schemas[table_name] = TableSchema(
                table_name=table_name,
                columns=columns,
            )

        return schemas

    # ============================================================
    # INSERT STATEMENT EXTRACTION
    # ============================================================

    def _extract_insert_statements(
        self,
        sql: str,
    ) -> list[dict[str, str]]:

        statements: list[dict[str, str]] = []

        for match in self.INSERT_START_RE.finditer(sql):

            table_name = match.group("table")
            columns = match.group("columns")

            values_start = match.end()

            statement_end = self._find_statement_end(
                sql,
                values_start,
            )

            values = sql[
                values_start:statement_end
            ].strip()

            statements.append(
                {
                    "table": table_name,
                    "columns": columns or "",
                    "values": values,
                }
            )

        return statements

    @staticmethod
    def _find_statement_end(
        sql: str,
        start: int,
    ) -> int:

        """
        Find the SQL semicolon that is OUTSIDE a quoted string.

        This is critical because source data can contain things
        like URLs:

            https://example.com/path?a=1;b=2

        That semicolon must NOT terminate the INSERT statement.
        """

        in_string = False
        quote = ""
        escaped = False

        i = start

        while i < len(sql):

            char = sql[i]

            if in_string:

                if escaped:
                    escaped = False

                elif char == "\\":
                    escaped = True

                elif char == quote:

                    # SQL doubled quote:
                    #
                    # 'Master''s'
                    #
                    if (
                        i + 1 < len(sql)
                        and sql[i + 1] == quote
                    ):
                        i += 1

                    else:
                        in_string = False

            else:

                if char in ("'", '"'):

                    in_string = True
                    quote = char

                elif char == ";":

                    return i

            i += 1

        raise ValueError(
            "Could not find end of INSERT statement"
        )

    # ============================================================
    # IDENTIFIERS
    # ============================================================

    @staticmethod
    def _parse_identifier_list(
        value: str,
    ) -> list[str]:

        return [
            item.strip().strip("`")
            for item in value.split(",")
            if item.strip()
        ]

    # ============================================================
    # VALUES
    # ============================================================

    def _parse_value_tuples(
        self,
        text: str,
    ) -> list[list[Any]]:

        tuples: list[list[Any]] = []

        i = 0
        length = len(text)

        while i < length:

            while (
                i < length
                and text[i].isspace()
            ):
                i += 1

            if i >= length:
                break

            if text[i] != "(":
                raise ValueError(
                    "Expected '(' while parsing "
                    f"VALUES near: {text[i:i + 100]!r}"
                )

            tuple_text, i = (
                self._read_parenthesized(
                    text,
                    i,
                )
            )

            values = self._parse_tuple_values(
                tuple_text
            )

            tuples.append(values)

            while (
                i < length
                and text[i].isspace()
            ):
                i += 1

            if (
                i < length
                and text[i] == ","
            ):
                i += 1
                continue

            if i < length:
                raise ValueError(
                    "Unexpected character after "
                    f"VALUES tuple: {text[i]!r}"
                )

        return tuples

    # ============================================================
    # PARENTHESES
    # ============================================================

    @staticmethod
    def _read_parenthesized(
        text: str,
        start: int,
    ) -> tuple[str, int]:

        assert text[start] == "("

        depth = 0
        in_string = False
        quote = ""
        escaped = False

        i = start

        while i < len(text):

            char = text[i]

            if in_string:

                if escaped:
                    escaped = False

                elif char == "\\":
                    escaped = True

                elif char == quote:

                    # SQL doubled quote
                    if (
                        i + 1 < len(text)
                        and text[i + 1] == quote
                    ):
                        i += 1
                    else:
                        in_string = False

            else:

                if char in ("'", '"'):

                    in_string = True
                    quote = char

                elif char == "(":

                    depth += 1

                elif char == ")":

                    depth -= 1

                    if depth == 0:
                        return (
                            text[start + 1:i],
                            i + 1,
                        )

            i += 1

        raise ValueError(
            "Unclosed parenthesized VALUES tuple"
        )

    # ============================================================
    # INDIVIDUAL VALUES
    # ============================================================

    def _parse_tuple_values(
        self,
        text: str,
    ) -> list[Any]:

        values: list[str] = []

        current: list[str] = []

        in_string = False
        quote = ""
        escaped = False
        depth = 0

        i = 0

        while i < len(text):

            char = text[i]

            if in_string:

                current.append(char)

                if escaped:

                    escaped = False

                elif char == "\\":

                    escaped = True

                elif char == quote:

                    # SQL doubled quote
                    if (
                        i + 1 < len(text)
                        and text[i + 1] == quote
                    ):
                        current.append(
                            text[i + 1]
                        )
                        i += 1
                    else:
                        in_string = False

            else:

                if char in ("'", '"'):

                    in_string = True
                    quote = char

                    current.append(char)

                elif char in "([{":

                    depth += 1
                    current.append(char)

                elif char in ")]}":

                    depth -= 1
                    current.append(char)

                elif (
                    char == ","
                    and depth == 0
                ):

                    values.append(
                        "".join(current).strip()
                    )

                    current = []

                else:

                    current.append(char)

            i += 1

        values.append(
            "".join(current).strip()
        )

        return [
            self._convert_literal(value)
            for value in values
        ]

    # ============================================================
    # SQL LITERAL CONVERSION
    # ============================================================

    @staticmethod
    def _convert_literal(
        value: str,
    ) -> Any:

        value = value.strip()

        if value.upper() == "NULL":
            return None

        if (
            len(value) >= 2
            and value[0] in ("'", '"')
            and value[-1] == value[0]
        ):

            quote = value[0]
            content = value[1:-1]

            # MySQL-style escapes
            content = content.replace(
                "\\'",
                "'",
            )

            content = content.replace(
                '\\"',
                '"',
            )

            content = content.replace(
                "\\\\",
                "\\",
            )

            content = content.replace(
                "\\n",
                "\n",
            )

            content = content.replace(
                "\\r",
                "\r",
            )

            content = content.replace(
                "\\t",
                "\t",
            )

            # SQL doubled quote
            content = content.replace(
                quote + quote,
                quote,
            )

            return content

        if re.fullmatch(
            r"-?\d+",
            value,
        ):
            return int(value)

        if re.fullmatch(
            r"-?\d+\.\d+",
            value,
        ):
            return Decimal(value)

        return value