"""Exercise 10: combine four Student Performance charts in one dashboard."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Create and save the required four-panel dashboard."""

    required_columns = [
        "Student",
        "Gender",
        "Study_Hours",
        "Math_Score",
    ]
    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        required_columns,
    )
    analysis_df = raw_df.copy()
    gender_counts = analysis_df["Gender"].value_counts()

    output_path = PROJECT_ROOT / "student-performance" / "outputs" / "10_mini_dashboard.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(12, 9))

    plt.subplot(2, 2, 1)
    plt.bar(analysis_df["Student"], analysis_df["Math_Score"], color="steelblue")
    plt.title("Math Scores by Student")
    plt.xlabel("Student")
    plt.ylabel("Score")
    plt.ylim(0, 100)
    plt.xticks(rotation=30)

    plt.subplot(2, 2, 2)
    plt.pie(
        gender_counts,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        colors=["#4C78A8", "#F58518"],
        startangle=90,
    )
    plt.title("Gender Distribution")

    plt.subplot(2, 2, 3)
    plt.hist(
        analysis_df["Math_Score"],
        bins=5,
        color="mediumpurple",
        edgecolor="white",
    )
    plt.title("Math Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Students")

    plt.subplot(2, 2, 4)
    plt.scatter(
        analysis_df["Study_Hours"],
        analysis_df["Math_Score"],
        color="crimson",
        s=65,
        alpha=0.8,
    )
    plt.title("Study Hours vs Math Score")
    plt.xlabel("Study hours")
    plt.ylabel("Math score")
    plt.ylim(0, 100)

    fig.suptitle("Student Performance Mini Dashboard", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved dashboard: {output_path}")
    print("Subplots created: 4")
    print("Layout method: plt.subplot()")


if __name__ == "__main__":
    main()
