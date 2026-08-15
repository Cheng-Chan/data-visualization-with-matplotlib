"""Small shared helpers for loading and identifying repository datasets."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import Path

import pandas as pd


def project_root() -> Path:
    """Return the repository root based on this module's location."""

    return Path(__file__).resolve().parents[1]


def load_dataset(
    relative_path: str | Path,
    required_columns: Sequence[str],
) -> tuple[Path, pd.DataFrame]:
    """Load a repository CSV and check that required columns are present."""

    dataset_path = project_root() / relative_path
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    dataframe = pd.read_csv(dataset_path)
    missing_columns = [
        column for column in required_columns if column not in dataframe.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns {missing_columns}: {dataset_path}"
        )

    return dataset_path, dataframe


def sha256(path: Path) -> str:
    """Return the SHA-256 hash of a file without changing it."""

    return hashlib.sha256(path.read_bytes()).hexdigest()
