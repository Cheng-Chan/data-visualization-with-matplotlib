"""NBA Exercise 6: inspect the historical salary distribution."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def currency_in_millions(value: float, _position: int) -> str:
    """Format a salary axis tick in millions of dollars."""

    return f"${value / 1_000_000:.0f}M"


def main() -> None:
    """Calculate salary statistics and save the required histogram."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Salary"],
    )
    analysis_df = raw_df.copy()
    salary = analysis_df["Salary"]
    quartiles = salary.quantile([0.25, 0.50, 0.75])
    median_salary = quartiles.loc[0.50]
    apparent_imputed_count = salary.eq(median_salary).sum()

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "06_salary_histogram.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    counts, _, _ = ax.hist(
        salary,
        bins=10,
        color="#457B9D",
        edgecolor="white",
    )
    ax.set_title("Salary Distribution — Historical Dataset Values")
    ax.set_xlabel("Salary (USD)")
    ax.set_ylabel("Number of players")
    ax.xaxis.set_major_formatter(FuncFormatter(currency_in_millions))
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Number of bins: {len(counts)}")
    print(f"Minimum: ${salary.min():,.0f}")
    print(f"Maximum: ${salary.max():,.0f}")
    print(f"Mean: ${salary.mean():,.0f}")
    print(f"Median: ${median_salary:,.0f}")
    print(f"First quartile: ${quartiles.loc[0.25]:,.0f}")
    print(f"Third quartile: ${quartiles.loc[0.75]:,.0f}")
    print(f"Skewness: {salary.skew():.3f}")
    print(f"Values above third quartile: {(salary > quartiles.loc[0.75]).mean():.1%}")
    print(
        "Apparent median-imputed salary values: "
        f"{apparent_imputed_count} (provenance is not encoded in the CSV)"
    )


if __name__ == "__main__":
    main()
