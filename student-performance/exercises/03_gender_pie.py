"""Exercise 3: show the gender composition with a pie chart."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def main() -> None:
    """Load the data and save the gender composition chart."""

    _, raw_df = load_dataset(
        "student-performance/dataset/student_performance.csv",
        ["Gender"],
    )
    analysis_df = raw_df.copy()
    gender_counts = analysis_df["Gender"].value_counts()

    output_path = PROJECT_ROOT / "student-performance" / "outputs" / "03_gender_pie.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        gender_counts,
        labels=gender_counts.index,
        autopct="%1.1f%%",
        colors=["#4C78A8", "#F58518"],
        startangle=90,
    )
    ax.set_title("Gender Distribution of Students")
    ax.axis("equal")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Gender counts: {gender_counts.to_dict()}")
    print(f"Total students: {gender_counts.sum()}")


if __name__ == "__main__":
    main()
