"""Exercise 5: compare all three subject scores on one chart."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the multiple-subject line chart."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Student", "Math_Score", "English_Score", "Science_Score"],
    )
    analysis_df = raw_df.copy()

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "05_subject_scores_multiple_lines.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(
        analysis_df["Student"],
        analysis_df["Math_Score"],
        marker="o",
        color="#4C78A8",
        label="Math",
    )
    ax.plot(
        analysis_df["Student"],
        analysis_df["English_Score"],
        marker="o",
        color="#F58518",
        label="English",
    )
    ax.plot(
        analysis_df["Student"],
        analysis_df["Science_Score"],
        marker="o",
        color="#54A24B",
        label="Science",
    )
    ax.set_title("Subject Scores by Student")
    ax.set_xlabel("Student")
    ax.set_ylabel("Score (0–100)")
    ax.set_ylim(0, 100)
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Students plotted: {len(analysis_df)}")
    print(f"Subjects plotted: {['Math', 'English', 'Science']}")


if __name__ == "__main__":
    main()
