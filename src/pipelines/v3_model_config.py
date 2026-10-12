import json
from dataclasses import asdict
from pathlib import Path

from src.forecasting.model_config import (
    build_ridge_config,
)


OUTPUT_PATH = Path(
    "data/features/ridge_model_config.json"
)

REPORT_PATH = Path(
    "data/reports/ridge_model_config.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 30 - RIDGE MODEL CONFIGURATION")
    print("=" * 70)

    config = build_ridge_config(
        alpha=100.0
    )

    payload = asdict(config)

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            payload,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 30",
        "description": (
            "Reusable Ridge model configuration"
        ),
        **payload,
    }

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Model:                  "
        f"{config.model_name}"
    )
    print(
        f"Alpha:                  "
        f"{config.alpha}"
    )
    print(
        f"Feature count:          "
        f"{len(config.feature_columns)}"
    )
    print(
        f"Target:                 "
        f"{config.target_column}"
    )
    print(
        f"Validation days:        "
        f"{config.validation_days}"
    )

    print()
    print(
        f"Feature output:        "
        f"{OUTPUT_PATH.resolve()}"
    )
    print(
        f"Report:                "
        f"{REPORT_PATH.resolve()}"
    )

    print()
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()