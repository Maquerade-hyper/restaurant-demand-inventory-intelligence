from __future__ import annotations

import json
from pathlib import Path

from src.normalization.canonical import CanonicalNormalizer
from src.validation.canonical_integrity import (
    CanonicalIntegrityValidator,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EXTRACTED_DIR = PROJECT_ROOT / "data" / "extracted"
REPORT_DIR = PROJECT_ROOT / "data" / "reports"


def main() -> None:
    print("=" * 70)
    print("RESTAURANT DEMAND & INVENTORY INTELLIGENCE")
    print("V1 CANONICAL INTEGRITY")
    print("=" * 70)

    normalizer = CanonicalNormalizer(EXTRACTED_DIR)
    data = normalizer.normalize_all()

    validator = CanonicalIntegrityValidator(data)
    issues = validator.validate()

    errors = validator.errors()
    warnings = validator.warnings()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "status": "PASSED" if not errors else "ERRORS_FOUND",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "issues": [
            {
                "table": issue.table,
                "field": issue.field,
                "value": issue.value,
                "issue": issue.issue,
                "severity": issue.severity,
            }
            for issue in issues
        ],
    }

    report_path = REPORT_DIR / "canonical_integrity.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
            default=str,
        )

    print()
    print(f"Menus checked: {len(data['menus'])}")
    print(f"Orders checked: {len(data['orders'])}")
    print(f"Stock logs checked: {len(data['stock_logs'])}")
    print(
        "Stock requirements checked: "
        f"{len(data['stock_requirements'])}"
    )
    errors = validator.errors()
    warnings = validator.warnings()

    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Report: {report_path}")
    print()

    if errors:
        print("STATUS: ERRORS FOUND")

        for issue in errors[:20]:
            print(
                f"[ERROR] [{issue.table}] "
                f"{issue.field}={issue.value!r} "
                f"-> {issue.issue}"
            )

        return
    
    print("STATUS: PASSED")

    if warnings:
        print()
        print(f"Warnings detected: {len(warnings)}")

        for issue in warnings[:20]:
            print(
                f"[WARNING] [{issue.table}] "
                f"{issue.field}={issue.value!r} "
                f"-> {issue.issue}"
            )

    print()
    print("STATUS: PASSED")

    


if __name__ == "__main__":
    main()