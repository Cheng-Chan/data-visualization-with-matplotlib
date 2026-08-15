"""Exercise 7: examine the relationship between study hours and Math scores."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the Study Hours versus Math Score chart."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Study_Hours", "Math_Score"],
    )
    analysis_df = raw_df.copy()
    correlation = analysis_df["Study_Hours"].corr(analysis_df["Math_Score"])

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "07_study_hours_math_scatter.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(
        analysis_df["Study_Hours"],
        analysis_df["Math_Score"],
        color="crimson",
        marker="o",
        s=75,
        alpha=0.8,
        edgecolors="white",
        linewidths=0.7,
    )
    ax.set_title("Study Hours and Math Scores")
    ax.set_xlabel("Study hours")
    ax.set_ylabel("Math score (0–100)")
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.35)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Students plotted: {len(analysis_df)}")
    print(f"Pearson correlation (extension): {correlation:.3f}")


if __name__ == "__main__":
    main()
