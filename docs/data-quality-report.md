# Data Quality Report

This report records the read-only audit of the two repository datasets. The CSV files are raw source inputs for this project and must remain unchanged.

## Audit date and environment

- Python: 3.12.3
- Pandas: 3.0.5
- Matplotlib: 3.11.1
- Audit scripts:
  - `student-performance/exercises/00_data_audit.py`
  - `nba-players/exercises/00_data_audit.py`

## Filename mapping

The exercise documents use example filenames that do not exist in the repository.

| Exercise filename | Repository filename |
|---|---|
| `student_scores.csv` | `student-performance/dataset/student_performance.csv` |
| `nba_cleaned.csv` | `nba-players/dataset/nba_dataset.csv` |

The repository filenames are used directly. They are not renamed or duplicated.

## Student Performance dataset

Path: `student-performance/dataset/student_performance.csv`

| Property | Result |
|---|---|
| Shape | 10 rows × 7 columns |
| SHA-256 | `414fd7aebb628a51076bf630c9d6438b274c74011b095e115bc7151625beff0c` |
| Missing values | None |
| Duplicate rows | None |
| Duplicate students | None |
| Gender values | `Male`, `Female` |
| Study hours | 1–6, non-negative |
| Attendance | 70–98, within 0–100 |
| Math scores | 60–95, within 0–100 |
| English scores | 65–96, within 0–100 |
| Science scores | 58–94, within 0–100 |
| Whitespace issues | None |

Schema:

```text
Student         text
Gender          text
Study_Hours     integer
Attendance      integer
Math_Score      integer
English_Score   integer
Science_Score   integer
```

Decision:

```text
Cleaning required: No
Reason: Dataset passes the current validation rules.
```

The dataset still requires schema validation, type validation, range validation, duplicate validation, and documentation before analysis.

## NBA Players dataset

Path: `nba-players/dataset/nba_dataset.csv`

| Property | Result |
|---|---|
| Shape | 457 rows × 10 columns |
| SHA-256 | `21e004ac05408080888c37f2b716539ef15d127233e086f5e6bdf5905e012d79` |
| Current missing values | None |
| Duplicate rows | None |
| Duplicate names | None |
| Teams | 30 |
| Positions | `C`, `PF`, `PG`, `SF`, `SG` |
| Unknown colleges | 84, or 18.38% |
| Salary minimum | 30,888 |
| Salary maximum | 25,000,000 |
| Salary median | 2,839,073 |
| Age range | 19–40 |
| Weight range | 161–307 |
| Invalid height strings | None |
| Maximum `Height_m` difference | 0.005 meters |
| Team/position whitespace issues | None |

Schema:

```text
Name       text
Team       text
Number     float64, integer-like
Position   text
Age        float64, integer-like
Height     text in feet-inch format
Weight     float64, integer-like
College    text
Salary     float64, integer-like
Height_m   float64
```

All required validation checks passed.

Decision:

```text
Current missing values: none
Previously unavailable colleges: represented by Unknown
Previously unavailable salaries: apparently median-imputed
New destructive cleaning required: no
Analysis-specific preparation required: yes
```

## Evidence of previous NBA preparation

The current file appears to be a previously prepared derivative. Evidence is consistent with these earlier transformations:

1. One fully empty row was removed.
2. 84 unavailable college values were represented as `Unknown`.
3. 11 unavailable salary values appear to have been filled with the median salary, `2,839,073`.
4. `Height_m` was added as a derived column.

The repeated salary value and matching player names support this interpretation, but the current CSV does not contain a provenance flag. A repeated median value alone must not be treated as definitive proof of imputation.

## Preparation policy

Analysis scripts may create an explicit in-memory copy:

```python
raw_df = pd.read_csv(dataset_path)
analysis_df = raw_df.copy()
```

For the NBA analysis copy:

- Convert `Age`, `Weight`, and `Salary` to nullable integer types.
- Treat `Number` as a jersey identifier, not a measurement.
- Preserve `Height` as the formatted text value.
- Use `Height_m` for numerical calculations and plots.
- Keep `Unknown` as an explicit unavailable-information category.
- Apply filters only for the exercise that needs them.

## `Unknown` college policy

`Unknown` is not a college and must not be converted to zero, treated as a real college, or removed globally.

For the Top Colleges challenge:

1. Report the count and percentage of `Unknown` values.
2. Exclude only those rows from the college ranking.
3. Report that 84 of 457 rows were excluded.
4. Preserve the original DataFrame and source CSV.

Players with `Unknown` colleges remain available for salary, position, age, height, and weight analysis.

## Salary-imputation limitation

The required exercises use the repository’s supplied salary values. Interpretations involving salary must disclose that 11 values appear to have been median-imputed.

Median imputation can:

- Reduce natural variance.
- Create an artificial concentration at the median.
- Affect team averages and overall means.
- Affect correlations.
- Make unavailable salaries appear observed.

The required exercises will not silently remove these rows. A sensitivity comparison excluding verified imputed records is a possible later extension, but it is not part of the required workflow yet.

## Raw-data preservation policy

- Never overwrite either source CSV.
- Never create duplicate cleaned CSVs merely to satisfy the exercise filenames.
- Do not use unapproved global `dropna()`, `fillna()`, or `drop_duplicates()` operations.
- Verify both source hashes during final validation.
- Save charts separately from the source datasets.
