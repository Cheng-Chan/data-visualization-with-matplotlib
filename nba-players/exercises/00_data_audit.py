"""Read-only audit and lightweight preparation for the NBA Players dataset.

Run from any directory with:

    python nba-players/exercises/00_data_audit.py
"""

from __future__ import annotations

import re
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset, sha256  # noqa: E402


EXPECTED_COLUMNS = [
    "Name",
    "Team",
    "Number",
    "Position",
    "Age",
    "Height",
    "Weight",
    "College",
    "Salary",
    "Height_m",
]
APPROVED_POSITIONS = {"C", "PF", "PG", "SF", "SG"}
INTEGER_LIKE_COLUMNS = ["Number", "Age", "Weight", "Salary"]
HEIGHT_PATTERN = re.compile(r"^\d+-\d+$")


def height_to_meters(height: str) -> float:
    """Convert a feet-inch string such as ``6-2`` to meters."""

    feet, inches = height.split("-")
    return (int(feet) * 12 + int(inches)) * 0.0254


def validate_nba_data(df: pd.DataFrame) -> dict[str, bool]:
    """Run validation rules against the current repository data."""

    expected_height_m = df["Height"].map(height_to_meters)
    height_difference = (df["Height_m"] - expected_height_m).abs()

    return {
        "Name is non-null and unique": df["Name"].notna().all() and df["Name"].is_unique,
        "Team is non-null": df["Team"].notna().all(),
        "Position uses approved categories": df["Position"].isin(APPROVED_POSITIONS).all(),
        "Age is realistic": df["Age"].between(18, 60).all(),
        "Height matches feet-inch format": df["Height"].astype("string").str.fullmatch(HEIGHT_PATTERN).all(),
        "Weight is positive and realistic": df["Weight"].between(100, 400).all(),
        "Salary is positive": df["Salary"].gt(0).all(),
        "Height_m is realistic": df["Height_m"].between(1.5, 2.5).all(),
        "Height_m agrees within 0.01 meters": height_difference.le(0.01).all(),
        "There are no current missing values": not df.isna().any().any(),
        "There are no duplicate rows": not df.duplicated().any(),
        "There is no team or position whitespace": not any(
            df[column]
            .astype("string")
            .str.strip()
            .ne(df[column].astype("string"))
            .any()
            for column in ["Team", "Position"]
        ),
    }


def main() -> None:
    """Load, inspect, validate, and prepare an in-memory analysis copy."""

    dataset_path, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        EXPECTED_COLUMNS,
    )
    if list(raw_df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            "Unexpected NBA schema. "
            f"Expected {EXPECTED_COLUMNS}, found {list(raw_df.columns)}"
        )

    # Preparation changes only this in-memory copy; the raw CSV remains untouched.
    analysis_df = raw_df.copy()
    for column in INTEGER_LIKE_COLUMNS:
        analysis_df[column] = analysis_df[column].astype("Int64")

    unknown_college_count = raw_df["College"].eq("Unknown").sum()
    unknown_college_percentage = unknown_college_count / len(raw_df) * 100
    median_salary = raw_df["Salary"].median()
    median_salary_rows = raw_df.loc[raw_df["Salary"].eq(median_salary), "Name"]

    expected_height_m = raw_df["Height"].map(height_to_meters)
    height_difference = (raw_df["Height_m"] - expected_height_m).abs()
    fractional_counts = {
        column: int(raw_df[column].mod(1).ne(0).sum())
        for column in INTEGER_LIKE_COLUMNS
    }

    print("NBA Players Dataset — Read-Only Audit")
    print(f"Path: {dataset_path}")
    print(f"SHA-256: {sha256(dataset_path)}")
    print(f"Shape: {raw_df.shape[0]} rows × {raw_df.shape[1]} columns")
    print(f"Columns: {list(raw_df.columns)}")
    print("\nFirst five rows:")
    print(raw_df.head().to_string(index=False))
    print("\nRaw data types:")
    print(raw_df.dtypes.to_string())
    print("\nPrepared in-memory data types:")
    print(analysis_df.dtypes.to_string())
    print("\nMissing values by column:")
    print(raw_df.isna().sum().to_string())
    print(f"\nDuplicate rows: {raw_df.duplicated().sum()}")
    print(f"Duplicate player names: {raw_df['Name'].duplicated().sum()}")
    print(f"Teams: {raw_df['Team'].nunique()}")
    print(f"Position counts:\n{raw_df['Position'].value_counts().to_string()}")
    print(f"\nUnknown college count: {unknown_college_count}")
    print(f"Unknown college percentage: {unknown_college_percentage:.2f}%")
    print(f"Salary median: ${median_salary:,.0f}")
    print(f"Rows with salary equal to the median: {len(median_salary_rows)}")
    print(f"Names at the median salary:\n{median_salary_rows.to_list()}")
    print("\nFractional values in integer-like columns:")
    for column, count in fractional_counts.items():
        print(f"- {column}: {count}")
    print(f"Last row complete: {raw_df.iloc[-1].notna().all()}")
    print(f"Maximum Height_m conversion difference: {height_difference.max():.3f} meters")

    print("\nValidation results:")
    checks = validate_nba_data(raw_df)
    for description, passed in checks.items():
        print(f"- {'PASS' if passed else 'FAIL'}: {description}")

    all_checks_passed = all(checks.values())
    print("\nCurrent missing values: none" if raw_df.isna().sum().sum() == 0 else "\nCurrent missing values: present")
    print("Previously unavailable colleges: represented by Unknown")
    print("Previously unavailable salaries: apparently median-imputed")
    print("New destructive cleaning required: no" if all_checks_passed else "New destructive cleaning required: review")
    print("Analysis-specific preparation required: yes")
    print("Note: repeated median salaries are evidence consistent with prior imputation, not proof of provenance.")


if __name__ == "__main__":
    main()
