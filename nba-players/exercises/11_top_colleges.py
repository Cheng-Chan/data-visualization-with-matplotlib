"""NBA Challenge 11: rank colleges after transparent Unknown handling."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Report unavailable colleges and save the top-colleges chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Name", "College"],
    )
    analysis_df = raw_df.copy()
    unknown_mask = analysis_df["College"].eq("Unknown")
    unknown_count = int(unknown_mask.sum())
    unknown_percentage = unknown_count / len(analysis_df) * 100

    # Unknown is unavailable information, not a college. Filter only this ranking copy.
    college_df = analysis_df.loc[~unknown_mask].copy()
    top_colleges = college_df["College"].value_counts().head(10).sort_values()

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "11_top_colleges.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(
        top_colleges.index,
        top_colleges.values,
        color="#577590",
    )
    ax.set_title("Top 10 Colleges by Player Count")
    ax.set_xlabel("Number of players")
    ax.set_ylabel("College")
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Unknown college count: {unknown_count}")
    print(f"Unknown college percentage: {unknown_percentage:.2f}%")
    print(f"Rows excluded from college ranking: {unknown_count}")
    print("Unknown is unavailable information, not a college.")
    print("Top colleges:")
    for college, count in top_colleges.sort_values(ascending=False).items():
        print(f"- {college}: {count}")
    print(f"Original DataFrame rows preserved: {len(analysis_df) == len(raw_df)}")


if __name__ == "__main__":
    main()
