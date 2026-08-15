"""NBA Exercise 5: compare three differently scaled variables for 15 players."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Plot Age, Weight, and Height_m using the required shared axis."""

    required_columns = ["Name", "Age", "Weight", "Height_m"]
    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        required_columns,
    )
    analysis_df = raw_df.copy()
    first_15 = analysis_df.head(15)

    output_path = (
        PROJECT_ROOT
        / "nba-players"
        / "outputs"
        / "05_age_weight_height_lines.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(
        first_15["Name"],
        first_15["Age"],
        linestyle="-",
        color="#4C78A8",
        label="Age (years)",
    )
    ax.plot(
        first_15["Name"],
        first_15["Weight"],
        linestyle="--",
        color="#F58518",
        label="Weight (pounds)",
    )
    ax.plot(
        first_15["Name"],
        first_15["Height_m"],
        linestyle=":",
        color="#54A24B",
        label="Height_m (meters)",
    )
    ax.set_title("Age, Weight, and Height for the First 15 Players")
    ax.set_xlabel("Player")
    ax.set_ylabel("Value in source units")
    ax.tick_params(axis="x", rotation=60)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Players plotted: {len(first_15)}")
    print("Units: Age=years, Weight=pounds, Height_m=meters")
    print(
        "Weight range in chart: "
        f"{first_15['Weight'].min():.0f}–{first_15['Weight'].max():.0f} pounds"
    )
    print(
        "Height range in chart: "
        f"{first_15['Height_m'].min():.2f}–{first_15['Height_m'].max():.2f} meters"
    )


if __name__ == "__main__":
    main()
