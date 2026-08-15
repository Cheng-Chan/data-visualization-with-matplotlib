"""NBA Exercise 2: count players by position with horizontal bars."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Count positions and save the required horizontal bar chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Position"],
    )
    analysis_df = raw_df.copy()
    position_counts = analysis_df["Position"].value_counts().sort_values()

    output_path = (
        PROJECT_ROOT
        / "nba-players"
        / "outputs"
        / "02_position_counts_horizontal_bar.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(
        position_counts.index,
        position_counts.values,
        color="#E76F51",
    )
    ax.set_title("Player Count by Position")
    ax.set_xlabel("Number of players")
    ax.set_ylabel("Position")
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print("Position counts:")
    for position, count in position_counts.sort_values(ascending=False).items():
        print(f"- {position}: {count}")


if __name__ == "__main__":
    main()
