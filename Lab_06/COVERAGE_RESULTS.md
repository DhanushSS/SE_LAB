# Train fare coverage lab

Application: `Lab 6/train_fare.py` (unchanged).
Measured on 4 November 2026 with Python 3.15.2, pytest 9.2.0,
and coverage.py 7.17.1. Screenshots show real VS Code terminal runs.

| Stage | Tests passed | Lines | Branch outcomes |
| --- | ---: | ---: | ---: |
| Original `test_train_fare.py` | 2 | 14/31 (45.16%) | 7/22 (31.82%) |
| Code coverage suite | 17 | 31/31 (100%) | Not measured in line-only run |
| Branch coverage suite | 47 | 31/31 (100%) | 22/22 (100%) |

The original branch-mode report displays 40%: coverage.py combines
line and branch counts, `(14 + 7) / (31 + 22)`. Actual branch-only
coverage is `7 / 22`. The final branch suite has no missing lines,
missing branches, partial branches, or excluded lines.

## Reproduce

From the repository root, create and activate a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cd 'Lab 6'
```

Original baseline (do not submit baseline screenshots):

```sh
coverage run --source=train_fare -m pytest test_train_fare.py
coverage report -m
coverage run --branch --source=train_fare -m pytest test_train_fare.py
coverage report -m
```

Code coverage:

```sh
coverage run --source=train_fare -m pytest CodeCoverageTest_train_fare_application.py
coverage report -m --fail-under=90
```

Branch coverage:

```sh
coverage run --branch --source=train_fare -m pytest BranchCoverageTest_train_fare_application.py
coverage report -m --fail-under=90
coverage json -o ../evidence/branch_coverage.json
```

Reports measure only the application, not test code. The branch report's
100% also confirms 100% branch-only coverage in the JSON report.
Run `pytest` from the repository root to collect both submission suites
and the preserved original tests (66 cases total).

## Test design

The code suite checks every fare rate, the minimum fare, both validation
errors, all concession return values, both Tatkal rates, and charge limits.
The branch suite independently checks both outcomes of every decision,
including ages 4/5, 12/13, 59/60, senior gender outcomes, Tatkal overrides,
minimum-fare equality, charge floor/cap equality, and integer rounding.
Invalid class takes precedence over invalid distance, as the code specifies.

## Submission files

- `evidence/coverage_results_combined.png`: both passing terminal results.
- `Lab 6/CodeCoverageTest_train_fare_application.py`: line coverage tests.
- `Lab 6/BranchCoverageTest_train_fare_application.py`: branch coverage tests.
- `../commits_terminal.png`: proof of the two local commits, alongside the clone.

The two separate commits each include their own test suite and terminal
screenshot. Remote publication requires repository write access; local
commit evidence alone does not prove a push to GitHub.
