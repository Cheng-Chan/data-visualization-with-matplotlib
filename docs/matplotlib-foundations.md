# Matplotlib Foundations

## What visualization does

Visualization turns columns of data into a visual representation that helps us compare, inspect, and communicate evidence. A chart is not decoration: its design should match the analytical question.

For the first Student Performance exercise, the question is:

> How do the students' Math scores compare?

This is a comparison of categories and numeric measurements, so a bar chart is an appropriate starting point.

## The Matplotlib object model

- A `Figure` is the complete canvas.
- An `Axes` is one plotting area inside the Figure.
- `pyplot` provides convenient functions and display utilities.
- The object-oriented API keeps the Figure and Axes explicit, which is easier to maintain as dashboards become more complex.

The basic flow is:

```python
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(x_values, y_values, color="steelblue")
ax.set_title("Math Scores by Student")
ax.set_xlabel("Student")
ax.set_ylabel("Math score")
fig.tight_layout()
fig.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close(fig)
```

Important choices:

- `figsize` controls the physical size of the Figure.
- `color` changes the bar appearance.
- Axis labels explain what each dimension represents.
- `tight_layout()` reduces clipping and overlap.
- `dpi=150` controls output resolution.
- `bbox_inches="tight"` includes labels near the edges.
- `plt.close(fig)` releases the Figure after saving.

## Demonstration code

This is a foundation demonstration, not yet the completed exercise script:

```python
from pathlib import Path

import matplotlib.pyplot as plt
from common.data_loading import load_dataset

required_columns = ["Student", "Math_Score"]
_, raw_df = load_dataset(
    "student-performance/dataset/student_performance.csv",
    required_columns,
)
analysis_df = raw_df.copy()

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(
    analysis_df["Student"],
    analysis_df["Math_Score"],
    color="steelblue",
)
ax.set_title("Math Scores by Student")
ax.set_xlabel("Student")
ax.set_ylabel("Math score")
fig.tight_layout()

output_path = Path("student-performance/outputs/foundation_demo.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output_path, dpi=150, bbox_inches="tight")
plt.close(fig)
```

The student names are categories, not a continuous numerical x-axis. The bars compare individual values, and the zero baseline makes bar lengths meaningful.

## Stateful versus object-oriented style

The stateful style is concise:

```python
plt.bar(df["Student"], df["Math_Score"])
plt.title("Math Scores by Student")
```

The object-oriented style is preferred for this project:

```python
fig, ax = plt.subplots()
ax.bar(df["Student"], df["Math_Score"])
ax.set_title("Math Scores by Student")
```

The second style makes it clear which Axes receives each setting and scales naturally to multiple charts.

## Chart reading checklist

Before interpreting a chart, ask:

1. What does each axis represent?
2. What are the units?
3. Are categories ordered meaningfully?
4. Is the chart showing comparison, distribution, composition, trend, or relationship?
5. What does the chart show directly?
6. What cannot be concluded from it?

The 10-row Student Performance dataset is useful for learning chart mechanics, but it is too small for broad educational conclusions.
