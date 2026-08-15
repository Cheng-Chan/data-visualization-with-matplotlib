"""NBA bonus 2: analyze a user-selected team's roster."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


TEAM_NAME = "New York Knicks"


def currency_in_millions(value: float, _position: int) -> str:
    """Format a salary axis tick in millions of dollars."""

    return f"${value / 1_000_000:.1f}M"


def main() -> None:
    """Create age, salary, and position charts for the selected team."""

    required_columns = ["Team", "Position", "Age", "Salary"]
    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        required_columns,
    )
    analysis_df = raw_df.copy()
    team_df = analysis_df.loc[analysis_df["Team"].eq(TEAM_NAME)].copy()
    if team_df.empty:
        raise ValueError(f"Selected team not found: {TEAM_NAME}")

    position_counts = team_df["Position"].value_counts().sort_values()
    age_by_position = team_df.groupby("Position")["Age"].mean().sort_values()
    salary_by_position = team_df.groupby("Position")["Salary"].mean().sort_values()

    output_path = (
        PROJECT_ROOT
        / "nba-players"
        / "outputs"
        / "bonus_02_new_york_knicks_analysis.png"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.5))

    axes[0].bar(
        age_by_position.index,
        age_by_position.values,
        color="#4C78A8",
    )
    axes[0].set_title("Average Age by Position")
    axes[0].set_xlabel("Position")
    axes[0].set_ylabel("Age (years)")

    axes[1].bar(
        salary_by_position.index,
        salary_by_position.values,
        color="#2A9D8F",
    )
    axes[1].set_title("Average Salary by Position")
    axes[1].set_xlabel("Position")
    axes[1].set_ylabel("Mean salary (USD)")
    axes[1].yaxis.set_major_formatter(FuncFormatter(currency_in_millions))

    axes[2].pie(
        position_counts,
        labels=position_counts.index,
        autopct="%1.1f%%",
        colors=["#F58518", "#E45756", "#72B7B2", "#B279A2", "#59A14F"],
        startangle=90,
    )
    axes[2].set_title("Position Distribution")
    axes[2].axis("equal")

    fig.suptitle(f"{TEAM_NAME} Team Analysis", fontsize=16)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved team analysis: {output_path}")
    print(f"Team: {TEAM_NAME}")
    print(f"Players: {len(team_df)}")
    print(f"Average age: {team_df['Age'].mean():.1f} years")
    print(f"Average salary: ${team_df['Salary'].mean():,.0f}")
    print(f"Position counts: {position_counts.sort_values(ascending=False).to_dict()}")
    print("Salary values include the repository's apparent median-imputation limitation.")


if __name__ == "__main__":
    main()
