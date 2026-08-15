"""Exercise 8: examine Attendance and Science score together."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the customized Attendance scatter plot."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Attendance", "Science_Score"],
    )
    analysis_df = raw_df.copy()
    correlation = analysis_df["Attendance"].corr(analysis_df["Science_Score"])

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "08_attendance_science_scatter.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(
        analysis_df["Attendance"],
        analysis_df["Science_Score"],
        color="darkviolet",
        marker="^",
        s=130,
        alpha=0.8,
        edgecolors="white",
        linewidths=0.7,
    )
    ax.set_title("Attendance and Science Scores")
    ax.set_xlabel("Attendance (%)")
    ax.set_ylabel("Science score (0–100)")
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
