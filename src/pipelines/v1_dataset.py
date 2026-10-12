from pathlib import Path

from src.dataset.canonical_dataset import CanonicalDataset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CANONICAL_DIR = PROJECT_ROOT / "data" / "canonical"


def main() -> None:
    dataset = CanonicalDataset(CANONICAL_DIR)

    counts = dataset.counts()

    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1 CANONICAL DATASET")
    print("=" * 70)

    for table, count in counts.items():
        print(f"{table:<25} {count:>6} rows")

    data = dataset.load()

    if not data:
        raise RuntimeError("Canonical dataset is empty")

    print()
    print("Tables loaded:", len(data))
    print("STATUS: PASSED")


if __name__ == "__main__":
    main()