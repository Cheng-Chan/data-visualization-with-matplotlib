"""Student bonus 2: experiment with purposeful chart styling."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Create a small board of readable style experiments."""

    required_columns = [
        "Student",
        "Study_Hours",
        "Math_Score",
        "English_Score",
        "Science_Score",
    ]
    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        required_columns,
    )
    analysis_df = raw_df.copy()

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "bonus_02_style_experiments.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))

    # Color and edge contrast make the category comparison easy to scan.
    axes[0].bar(
        analysis_df["Student"],
        analysis_df["Math_Score"],
        color="#3366CC",
        edgecolor="#1F2D5A",
    )
    axes[0].set_title("High-Contrast Bars")
    axes[0].set_xlabel("Student")
    axes[0].set_ylabel("Math score")
    axes[0].set_ylim(0, 100)
    axes[0].tick_params(axis="x", rotation=60)

    # Markers and linestyles distinguish subject series in a shared chart.
    line_styles = [
        ("Math_Score", "o", "-", "#4C78A8"),
        ("English_Score", "s", "--", "#F58518"),
        ("Science_Score", "^", ":", "#54A24B"),
    ]
    for column, marker, linestyle, color in line_styles:
        axes[1].plot(
            analysis_df["Student"],
            analysis_df[column],
            marker=marker,
            linestyle=linestyle,
            color=color,
            label=column.replace("_Score", ""),
        )
    axes[1].set_title("Markers and Linestyles")
    axes[1].set_xlabel("Student")
    axes[1].set_ylabel("Score")
    axes[1].set_ylim(0, 100)
    axes[1].tick_params(axis="x", rotation=60)
    axes[1].legend()

    # A diamond marker and transparency help separate overlapping observations.
    axes[2].scatter(
        analysis_df["Study_Hours"],
        analysis_df["Math_Score"],
        color="#C44E52",
        marker="D",
        s=90,
        alpha=0.75,
        edgecolors="white",
    )
    axes[2].set_title("Readable Scatter Styling")
    axes[2].set_xlabel("Study hours")
    axes[2].set_ylabel("Math score")
    axes[2].set_ylim(0, 100)
    axes[2].grid(alpha=0.3)

    fig.suptitle("Purposeful Matplotlib Style Experiments", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved style board: {output_path}")
    print("Experiments: colors, markers, linestyles, figure size")


if __name__ == "__main__":
    main()
