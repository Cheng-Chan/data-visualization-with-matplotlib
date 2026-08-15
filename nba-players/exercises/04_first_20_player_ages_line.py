"""NBA Exercise 4: plot ages for the first 20 dataset rows."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Select the first 20 rows and save the required age line chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Name", "Age"],
    )
    analysis_df = raw_df.copy()
    first_20 = analysis_df.head(20)

    output_path = (
        PROJECT_ROOT
        / "nba-players"
        / "outputs"
        / "04_first_20_player_ages_line.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        first_20["Name"],
        first_20["Age"],
        marker="o",
        linestyle="-.",
        color="#577590",
        label="Age",
    )
    ax.set_title("Ages of the First 20 Players in Dataset Order")
    ax.set_xlabel("Player")
    ax.set_ylabel("Age (years)")
    ax.tick_params(axis="x", rotation=60)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Players plotted: {len(first_20)}")
    print(f"Age range: {first_20['Age'].min():.0f}–{first_20['Age'].max():.0f}")
    print("The x-axis follows repository row order, not a time sequence.")


if __name__ == "__main__":
    main()
