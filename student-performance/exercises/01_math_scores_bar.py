"""Exercise 1: compare Student Performance math scores with a bar chart."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the required Math Score bar chart."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Student", "Math_Score"],
    )
    analysis_df = raw_df.copy()

    output_path = PROJECT_ROOT / "student-performance" / "outputs" / "01_math_scores_bar.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(
        analysis_df["Student"],
        analysis_df["Math_Score"],
        color="steelblue",
    )
    ax.set_title("Math Scores by Student")
    ax.set_xlabel("Student")
    ax.set_ylabel("Math score (0–100)")
    ax.set_ylim(0, 100)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Students plotted: {len(analysis_df)}")
    print(f"Score range: {analysis_df['Math_Score'].min()}–{analysis_df['Math_Score'].max()}")


if __name__ == "__main__":
    main()
