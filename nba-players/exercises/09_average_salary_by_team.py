"""NBA Exercise 9: compare average salary values by team."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from common.data_loading import load_dataset  # noqa: E402


def currency_in_millions(value: float, _position: int) -> str:
    """Format a salary axis tick in millions of dollars."""

    return f"${value / 1_000_000:.0f}M"


def main() -> None:
    """Aggregate salary by team and save the required horizontal chart."""

    _, raw_df = load_dataset(
        "nba-players/dataset/nba_dataset.csv",
        ["Team", "Salary"],
    )
    analysis_df = raw_df.copy()
    team_salary = analysis_df.groupby("Team")["Salary"].mean().sort_values()

    output_path = PROJECT_ROOT / "nba-players" / "outputs" / "09_average_salary_by_team.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 9))
    ax.barh(
        team_salary.index,
        team_salary.values,
        color="#2A9D8F",
    )
    ax.set_title("Average Salary by Team — Historical Dataset Values")
    ax.set_xlabel("Mean salary (USD)")
    ax.set_ylabel("Team")
    ax.xaxis.set_major_formatter(FuncFormatter(currency_in_millions))
    ax.grid(axis="x", linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved chart: {output_path}")
    print(f"Teams plotted: {len(team_salary)}")
    print(f"Lowest team mean: {team_salary.index[0]} (${team_salary.iloc[0]:,.0f})")
    print(f"Highest team mean: {team_salary.index[-1]} (${team_salary.iloc[-1]:,.0f})")
    print(
        "Interpretation must account for star-player salaries, roster sizes, "
        "and apparent imputation."
    )


if __name__ == "__main__":
    main()
