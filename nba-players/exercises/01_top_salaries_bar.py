"""NBA Exercise 1: chart the ten highest salary values in the dataset."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Select the top ten salaries and save the required bar chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Name", "Salary"],
    )
    analysis_df = raw_df.copy()
    top_salary = analysis_df.nlargest(10, "Salary")

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "01_top_salaries_bar.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(
        top_salary["Name"],
        top_salary["Salary"],
        color="#2A9D8F",
    )
    ax.set_title("Top 10 Salary Values in the NBA Dataset")
    ax.set_xlabel("Player")
    ax.set_ylabel("Salary (USD)")
    ax.yaxis.set_major_formatter(StrMethodFormatter("${x:,.0f}"))
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print("Top salary values:")
    for _, row in top_salary.iterrows():
        print(f"- {row['Name']}: ${row['Salary']:,.0f}")
    print("These are historical dataset values, not current salaries.")


if __name__ == "__main__":
    main()
