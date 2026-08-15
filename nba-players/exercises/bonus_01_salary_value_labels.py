"""NBA bonus 1: add salary labels above the top-salary bars."""

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
    """Create the annotated top-salary chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Name", "Salary"],
    )
    analysis_df = raw_df.copy()
    top_salary = analysis_df.nlargest(10, "Salary")

    output_path = (
        PROJECT_ROOT
        / "nba-players"
        / "outputs"
        / "bonus_01_top_salaries_value_labels.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.bar(top_salary["Name"], top_salary["Salary"], color="#2A9D8F")
    ax.set_title("Top 10 Salary Values — Labels Added")
    ax.set_xlabel("Player")
    ax.set_ylabel("Salary (USD)")
    ax.yaxis.set_major_formatter(FuncFormatter(currency_in_millions))
    ax.tick_params(axis="x", rotation=45)
    ax.set_ylim(0, top_salary["Salary"].max() * 1.12)

    for bar, salary in zip(bars, top_salary["Salary"]):
        ax.annotate(
            f"${salary / 1_000_000:.1f}M",
            xy=(bar.get_x() + bar.get_width() / 2, salary),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Salary labels added: {len(bars)}")


if __name__ == "__main__":
    main()
