"""Exercise 6: show the distribution of Math scores with five bins."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the required five-bin histogram."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Math_Score"],
    )
    analysis_df = raw_df.copy()

    output_path = (
        PROJECT_ROOT
        / "student-performance"
        / "outputs"
        / "06_math_score_histogram.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    counts, bin_edges, _ = ax.hist(
        analysis_df["Math_Score"],
        bins=5,
        color="mediumpurple",
        edgecolor="white",
    )
    ax.set_title("Distribution of Math Scores")
    ax.set_xlabel("Math score (0–100)")
    ax.set_ylabel("Number of students")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Number of bins: {len(counts)}")
    print(f"Bin counts: {[int(count) for count in counts]}")
    print(f"Bin edges: {[round(float(edge), 2) for edge in bin_edges]}")


if __name__ == "__main__":
    main()
