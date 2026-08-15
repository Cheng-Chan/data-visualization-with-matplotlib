"""Exercise 9: chart the average score for each subject."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Calculate subject means and save the average-score bar chart."""

    score_columns = ["Math_Score", "English_Score", "Science_Score"]
    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        score_columns,
    )
    analysis_df = raw_df.copy()
    average_scores = analysis_df[score_columns].mean()
    subject_labels = ["Math", "English", "Science"]

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "09_average_scores_bar.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        subject_labels,
        average_scores.values,
        color=["#4C78A8", "#F58518", "#54A24B"],
    )
    ax.set_title("Average Scores by Subject")
    ax.set_xlabel("Subject")
    ax.set_ylabel("Average score (0–100)")
    ax.set_ylim(0, 100)

    for bar, value in zip(bars, average_scores.values):
        ax.annotate(
            f"{value:.1f}",
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print("Average scores:")
    for subject, value in zip(subject_labels, average_scores.values):
        print(f"- {subject}: {value:.1f}")


if __name__ == "__main__":
    main()
