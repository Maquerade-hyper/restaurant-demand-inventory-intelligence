from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from typing import Any

from src.ingestion.sql_dump import SQLDumpParser
from src.validation.data_validator import DataValidator


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
EXTRACTED_DIR = PROJECT_ROOT / "data" / "extracted"
REPORT_DIR = PROJECT_ROOT / "data" / "reports"


INPUT_FILES = {
    "orders": "orders.sql",
    "menus": "menus.sql",
    "stock_managements": "stock_managements.sql",
    "stock_logs": "stock_logs.sql",
    "stock_requirements": "stock_requirements.sql",
}


def json_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return float(value)

    raise TypeError(
        f"Object of type {type(value).__name__} is not JSON serializable"
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
            default=json_default,
        ),
        encoding="utf-8",
    )


def run() -> None:
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    parser = SQLDumpParser()
    validator = DataValidator()

    all_reports: list[dict[str, Any]] = []
    schema_report: dict[str, Any] = {}

    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1.0 DATA FOUNDATION")
    print("=" * 70)

    for table_name, filename in INPUT_FILES.items():

        path = RAW_DIR / filename

        print(f"\n[{table_name}]")
        print(f"Reading: {path}")

        if not path.exists():
            raise FileNotFoundError(
                f"Required input file does not exist: {path}"
            )

        parsed = parser.parse_file(path)

        schema_report[table_name] = {
            "source_file": filename,
            "columns": parsed.schema.columns,
            "column_count": len(parsed.schema.columns),
            "row_count": len(parsed.rows),
        }

        extracted_path = EXTRACTED_DIR / f"{table_name}.json"

        write_json(
            extracted_path,
            {
                "table": table_name,
                "source_file": filename,
                "columns": parsed.schema.columns,
                "row_count": len(parsed.rows),
                "rows": parsed.rows,
            },
        )

        report = validator.validate(
            table_name,
            parsed.rows,
        )

        all_reports.append(report.to_dict())

        print(f"Columns : {len(parsed.schema.columns)}")
        print(f"Rows    : {len(parsed.rows)}")
        print(f"Errors  : {len(report.errors)}")
        print(f"Warnings: {len(report.warnings)}")

    quality_report = {
        "version": "V1.0",
        "status": (
            "passed"
            if not any(
                report["error_count"] > 0
                for report in all_reports
            )
            else "failed"
        ),
        "tables": all_reports,
    }

    write_json(
        REPORT_DIR / "data_quality.json",
        quality_report,
    )

    write_json(
        REPORT_DIR / "schema_report.json",
        schema_report,
    )

    print("\n" + "=" * 70)
    print("V1.0 INGESTION COMPLETE")
    print("=" * 70)

    print(f"Extracted data : {EXTRACTED_DIR}")
    print(f"Quality report : {REPORT_DIR / 'data_quality.json'}")
    print(f"Schema report  : {REPORT_DIR / 'schema_report.json'}")

    if quality_report["status"] == "failed":
        print("\nSTATUS: FAILED")
        print("Fix ingestion/validation errors before continuing.")
        raise SystemExit(1)

    print("\nSTATUS: PASSED")


if __name__ == "__main__":
    run()