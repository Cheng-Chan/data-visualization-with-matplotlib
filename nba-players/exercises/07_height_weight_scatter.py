"""NBA Exercise 7: examine the relationship between height and weight."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the Height_m versus Weight chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Height_m", "Weight"],
    )
    analysis_df = raw_df.copy()
    correlation = analysis_df["Height_m"].corr(analysis_df["Weight"])

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "07_height_weight_scatter.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.scatter(
        analysis_df["Height_m"],
        analysis_df["Weight"],
        color="#6A4C93",
        marker="D",
        s=60,
        alpha=0.75,
        edgecolors="white",
        linewidths=0.6,
    )
    ax.set_title("Height and Weight of NBA Players")
    ax.set_xlabel("Height (meters)")
    ax.set_ylabel("Weight (pounds)")
    ax.grid(alpha=0.35)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Players plotted: {len(analysis_df)}")
    print(f"Pearson correlation (extension): {correlation:.3f}")


if __name__ == "__main__":
    main()
