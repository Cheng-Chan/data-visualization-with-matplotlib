"""Student bonus 1: add values above Math score bars."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Create the annotated Math score bar chart."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Student", "Math_Score"],
    )
    analysis_df = raw_df.copy()

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "bonus_01_math_scores_value_labels.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(
        analysis_df["Student"],
        analysis_df["Math_Score"],
        color="steelblue",
    )
    ax.set_title("Math Scores by Student — Values Added")
    ax.set_xlabel("Student")
    ax.set_ylabel("Math score (0–100)")
    ax.set_ylim(0, 100)

    for bar, value in zip(bars, analysis_df["Math_Score"]):
        ax.annotate(
            str(value),
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
    print(f"Labels added: {len(bars)}")


if __name__ == "__main__":
    main()
