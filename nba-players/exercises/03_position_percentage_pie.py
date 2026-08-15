"""NBA Exercise 3: show the percentage of players by position."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Count positions and save the required percentage pie chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Position"],
    )
    analysis_df = raw_df.copy()
    position_counts = analysis_df["Position"].value_counts()
    position_percentages = position_counts / position_counts.sum() * 100

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "03_position_percentage_pie.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        position_counts,
        labels=position_counts.index,
        autopct="%1.1f%%",
        colors=["#4C78A8", "#F58518", "#E45756", "#72B7B2", "#B279A2"],
        startangle=90,
    )
    ax.set_title("Percentage of Players by Position")
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print("Position percentages:")
    for position, percentage in position_percentages.items():
        print(f"- {position}: {percentage:.1f}%")


if __name__ == "__main__":
    main()
