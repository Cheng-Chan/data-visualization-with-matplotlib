# Matplotlib Data Visualization — Zero to Hero

This repository contains guided Pandas and Matplotlib exercises using the Student Performance and NBA Players datasets.

## Project status

The source datasets have been audited and are preserved unchanged. Exercise scripts will be added incrementally, one approved phase at a time.

## Setup

The project uses Python 3.12 and a local virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Verify the environment with:

```bash
python --version
python -m pip --version
```

In VS Code, select the interpreter at `.venv/bin/python` (macOS/Linux) or `.venv\Scripts\python.exe` (Windows) using **Python: Select Interpreter**.

## Dataset paths

The exercise documents use example filenames that are not present in this repository. Use these repository paths instead:

| Exercise example | Repository path |
|---|---|
| `student_scores.csv` | `student-performance/dataset/student_performance.csv` |
| `nba_cleaned.csv` | `nba-players/dataset/nba_dataset.csv` |

Do not rename, overwrite, or duplicate the source CSV files. Analysis code should build an in-memory copy when preparation is needed.

## Output policy

Exercise scripts create their output directory at runtime and save reviewable PNG charts there. Generated outputs are intentionally eligible for Git tracking so the charts can be reviewed from the repository:

```text
student-performance/outputs/
nba-players/outputs/
```

Source datasets and explanatory documentation remain tracked.

## Running the audits

Run either audit from the repository root or from another working directory:

```bash
python student-performance/exercises/00_data_audit.py
python nba-players/exercises/00_data_audit.py
```

## Running the exercises

Student Performance exercises:

```bash
python student-performance/exercises/01_math_scores_bar.py
python student-performance/exercises/10_mini_dashboard.py
```

NBA exercises:

```bash
python nba-players/exercises/01_top_salaries_bar.py
python nba-players/exercises/10_mini_dashboard.py
python nba-players/exercises/11_top_colleges.py
```

Run the other numbered or bonus scripts in the same way. Each script saves its PNG output under the corresponding `outputs/` directory.

## Dependencies

Direct dependencies are pinned in [requirements.txt](requirements.txt):

- Pandas for DataFrames, validation, aggregation, and preparation.
- Matplotlib for chart creation and saving.

## Learning workflow

The canonical implementations will be Python scripts. Each exercise will document its analytical question, data preparation, visualization choices, execution result, interpretation, critique, and limitations.
