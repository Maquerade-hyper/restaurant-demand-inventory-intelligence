import json
from pathlib import Path
from typing import Any


class InventoryPackageJsonStore:

    def save(
        self,
        package: Any,
        path: str | Path,
    ) -> Path:

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        payload = package.to_dict()

        output_path.write_text(
            json.dumps(
                payload,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        return output_path

    def load(
        self,
        path: str | Path,
    ) -> dict[str, Any]:

        input_path = Path(path)

        if not input_path.exists():
            raise FileNotFoundError(str(input_path))

        return json.loads(
            input_path.read_text(encoding="utf-8")
        )
