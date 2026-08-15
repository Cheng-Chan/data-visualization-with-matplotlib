"""Exercise 2: compare English scores with a horizontal bar chart."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the required English Score chart."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Student", "English_Score"],
    )
    analysis_df = raw_df.copy()

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "02_english_scores_horizontal_bar.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(
        analysis_df["Student"],
        analysis_df["English_Score"],
        color="darkorange",
    )
    ax.invert_yaxis()
    ax.set_title("English Scores by Student")
    ax.set_xlabel("English score (0–100)")
    ax.set_ylabel("Student")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Students plotted: {len(analysis_df)}")
    print(
        "Score range: "
        f"{analysis_df['English_Score'].min()}–{analysis_df['English_Score'].max()}"
    )


if __name__ == "__main__":
    main()
