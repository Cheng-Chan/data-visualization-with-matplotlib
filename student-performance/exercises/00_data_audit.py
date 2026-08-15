"""Read-only audit for the Student Performance dataset.

Run from any directory with:

    python student-performance/exercises/00_data_audit.py
"""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset, sha256  # noqa: E402


EXPECTED_COLUMNS = [
    "Student",
    "Gender",
    "Study_Hours",
    "Attendance",
    "Math_Score",
    "English_Score",
    "Science_Score",
]
APPROVED_GENDERS = {"Male", "Female"}
SCORE_COLUMNS = ["Math_Score", "English_Score", "Science_Score"]


def check_student_data(df: pd.DataFrame) -> dict[str, bool]:
    """Run the exercise-specific validation rules."""

    return {
        "Student is non-null and unique": df["Student"].notna().all()
        and df["Student"].is_unique,
        "Gender uses approved categories": df["Gender"].isin(APPROVED_GENDERS).all(),
        "Study_Hours is non-negative": df["Study_Hours"].ge(0).all(),
        "Attendance is between 0 and 100": df["Attendance"].between(0, 100).all(),
        "All subject scores are between 0 and 100": df[SCORE_COLUMNS]
        .apply(lambda column: column.between(0, 100).all())
        .all(),
        "There are no missing values": not df.isna().any().any(),
        "There are no duplicate rows": not df.duplicated().any(),
        "There is no leading or trailing whitespace": not any(
            df[column]
            .astype("string")
            .str.strip()
            .ne(df[column].astype("string"))
            .any()
            for column in ["Student", "Gender"]
        ),
    }


def main() -> None:
    """Load, inspect, and validate the dataset without modifying it."""

    dataset_path, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        EXPECTED_COLUMNS,
    )
    analysis_df = raw_df.copy()

    print("Student Performance Dataset — Read-Only Audit")
    print(f"Path: {dataset_path}")
    print(f"SHA-256: {sha256(dataset_path)}")
    print(f"Shape: {raw_df.shape[0]} rows × {raw_df.shape[1]} columns")
    print(f"Columns: {list(raw_df.columns)}")
    print("\nFirst five rows:")
    print(raw_df.head().to_string(index=False))
    print("\nData types:")
    print(raw_df.dtypes.to_string())
    print("\nMissing values by column:")
    print(raw_df.isna().sum().to_string())
    print(f"\nDuplicate rows: {raw_df.duplicated().sum()}")
    print(f"Duplicate student names: {raw_df['Student'].duplicated().sum()}")
    print(f"Gender counts:\n{raw_df['Gender'].value_counts().to_string()}")
    print("\nNumeric summary:")
    print(raw_df.describe().to_string())

    schema_matches = list(raw_df.columns) == EXPECTED_COLUMNS
    print(f"\nSchema matches expected columns: {schema_matches}")

    print("\nValidation results:")
    checks = check_student_data(analysis_df)
    for description, passed in checks.items():
        print(f"- {'PASS' if passed else 'FAIL'}: {description}")

    all_checks_passed = schema_matches and all(checks.values())
    print("\nCleaning required: No" if all_checks_passed else "\nCleaning required: Review")
    if all_checks_passed:
        print("Reason: Dataset passes the current validation rules.")
    else:
        print("Reason: One or more schema or validation checks failed.")


if __name__ == "__main__":
    main()
