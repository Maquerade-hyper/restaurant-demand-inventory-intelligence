import json
from pathlib import Path

from src.forecasting.training_split import (
    ChronologicalTrainingSplitter,
)


INPUT_PATH = Path(
    "data/features/feature_matrix.json"
)

OUTPUT_PATH = Path(
    "data/features/training_split.json"
)

REPORT_PATH = Path(
    "data/reports/training_split.json"
)


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V3 PART 24 - TRAINING DATASET SPLIT")
    print("=" * 70)

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Missing input file: {INPUT_PATH}"
        )

    payload = json.loads(
        INPUT_PATH.read_text(encoding="utf-8")
    )

    rows = payload["rows"]

    splitter = ChronologicalTrainingSplitter(
        rows,
        validation_days=14,
    )

    split = splitter.split()

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
            {
                "train": split.train,
                "validation": split.validation,
                "cutoff_date": split.cutoff_date,
                "validation_days": 14,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    report = {
        "part": "V3 Part 24",
        "description": (
            "Chronological training and validation split"
        ),
        "input_rows": len(rows),
        "train_rows": len(split.train),
        "validation_rows": len(split.validation),
        "validation_days": 14,
        "cutoff_date": split.cutoff_date,
        "train_max_date": max(
            str(row["date"])
            for row in split.train
        ),
        "validation_min_date": min(
            str(row["date"])
            for row in split.validation
        ),
    }

    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"Input rows:             {len(rows):,}")
    print(f"Training rows:          {len(split.train):,}")
    print(
        f"Validation rows:       "
        f"{len(split.validation):,}"
    )
    print(f"Validation days:       14")
    print(f"Cutoff date:           {split.cutoff_date}")
    print(
        f"Training max date:     "
        f"{report['train_max_date']}"
    )
    print(
        f"Validation min date:   "
        f"{report['validation_min_date']}"
    )

    assert (
        report["train_max_date"]
        < report["validation_min_date"]
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