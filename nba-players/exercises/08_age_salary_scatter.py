"""NBA Exercise 8: examine age and salary together."""

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
    """Load the data and save the Age versus Salary scatter plot."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Age", "Salary"],
    )
    analysis_df = raw_df.copy()
    correlation = analysis_df["Age"].corr(analysis_df["Salary"])
    median_salary = analysis_df["Salary"].median()
    apparent_imputed_count = analysis_df["Salary"].eq(median_salary).sum()

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "08_age_salary_scatter.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.scatter(
        analysis_df["Age"],
        analysis_df["Salary"],
        color="#E76F51",
        marker="o",
        s=80,
        alpha=0.55,
        edgecolors="white",
        linewidths=0.5,
    )
    ax.set_title("Age and Salary — Historical Dataset Values")
    ax.set_xlabel("Age (years)")
    ax.set_ylabel("Salary (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(currency_in_millions))
    ax.grid(alpha=0.35)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Players plotted: {len(analysis_df)}")
    print(f"Pearson correlation (extension): {correlation:.3f}")
    print(f"Apparent median-imputed salary values: {apparent_imputed_count}")
    print("Salary provenance is not encoded in the CSV.")


if __name__ == "__main__":
    main()
