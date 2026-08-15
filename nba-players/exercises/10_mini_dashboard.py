"""NBA Exercise 10: combine four NBA charts in one dashboard."""

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
    """Create and save the required four-panel NBA dashboard."""

    required_columns = [
        "Name",
        "Position",
        "Salary",
        "Height_m",
        "Weight",
    ]
    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        required_columns,
    )
    analysis_df = raw_df.copy()
    top_salary = analysis_df.nlargest(10, "Salary")
    position_counts = analysis_df["Position"].value_counts()

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "10_mini_dashboard.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.bar(top_salary["Name"], top_salary["Salary"], color="#2A9D8F")
    plt.title("Top 10 Salary Values")
    plt.xlabel("Player")
    plt.ylabel("Salary (USD)")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(currency_in_millions))
    plt.xticks(rotation=60, ha="right")

    plt.subplot(2, 2, 2)
    plt.pie(
        position_counts,
        labels=position_counts.index,
        autopct="%1.1f%%",
        colors=["#4C78A8", "#F58518", "#E45756", "#72B7B2", "#B279A2"],
        startangle=90,
    )
    plt.title("Player Percentage by Position")

    plt.subplot(2, 2, 3)
    plt.hist(
        analysis_df["Salary"],
        bins=10,
        color="#457B9D",
        edgecolor="white",
    )
    plt.title("Salary Distribution")
    plt.xlabel("Salary (USD)")
    plt.ylabel("Players")
    plt.gca().xaxis.set_major_formatter(FuncFormatter(currency_in_millions))

    plt.subplot(2, 2, 4)
    plt.scatter(
        analysis_df["Height_m"],
        analysis_df["Weight"],
        color="#6A4C93",
        marker="D",
        s=45,
        alpha=0.6,
        edgecolors="white",
        linewidths=0.4,
    )
    plt.title("Height and Weight")
    plt.xlabel("Height (meters)")
    plt.ylabel("Weight (pounds)")

    fig.suptitle("NBA Players Mini Dashboard — Historical Dataset", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved dashboard: {output_path}")
    print("Subplots created: 4")
    print("Layout method: plt.subplot()")
    print("Salary panels use supplied values, including 11 apparently imputed salaries.")


if __name__ == "__main__":
    main()
