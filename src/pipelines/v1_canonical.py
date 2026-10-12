from __future__ import annotations

from pathlib import Path

from src.normalization.canonical import (
    CanonicalNormalizer,
    write_canonical,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EXTRACTED_DIR = PROJECT_ROOT / "data" / "extracted"
CANONICAL_DIR = PROJECT_ROOT / "data" / "canonical"


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1 CANONICAL NORMALIZATION")
    print("=" * 70)

    normalizer = CanonicalNormalizer(EXTRACTED_DIR)

    data = normalizer.normalize_all()

    write_canonical(
        data=data,
        output_dir=CANONICAL_DIR,
    )

    print()

    for table, records in data.items():
        print(f"{table:<25} {len(records):>6} rows")

    print()
    print("=" * 70)
    print("CANONICAL NORMALIZATION COMPLETE")
    print("=" * 70)
    print(f"Output: {CANONICAL_DIR}")
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()