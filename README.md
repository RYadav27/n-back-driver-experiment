# N-Back Driver Experiment

A local Windows application for conducting 0-back, 1-back and 2-back number-listening tasks, with a live single-screen dashboard for the observer to monitor the driver in real time.

## Experimental setup

- Driver listens to spoken numbers.
- Driver responds verbally.
- Observer/researcher sits in the side seat and watches the dashboard.
- Observer presses:
  - `M` = Match
  - `N` = No Match
  - `S` = Skip
- The computer produces audio for numbers only. M/N/S keys are silent to the driver.
- The driver's voice can be recorded independently by the eye-tracker system.

## Task structure

Each run contains exactly 20 numbers.

Available tasks:

- 0-Back
- 1-Back
- 2-Back

The intended stimulus-onset interval is 2.25 seconds.

For 1-back, the observer skips the first trial. For 2-back, the observer skips the first two trials. Skipped trials are excluded from the accuracy calculation.

## Dashboard

The app opens a Streamlit dashboard sized to fit a single screen with no scrolling, so the observer can monitor the driver without looking away.

Start screen shows:

- Driver number selector
- Trial count, stimulus-onset interval, and audio type at a glance
- Observer key reference (M / N / S)
- The exact filename the next run will be saved as

During a run, the dashboard shows:

- Live trial progress (e.g. `12 / 20`)
- The current spoken number
- Running Match / No Match / Skip counts
- Live accuracy
- Observer response buttons and a Stop Run button

## Excel output

Every run is saved automatically as a new Excel file, named by driver and run number:

```text
data/
├── D1_run01.xlsx
├── D1_run02.xlsx
├── D1_run03.xlsx
├── D2_run01.xlsx
└── D2_run02.xlsx
```

The run number for each driver is calculated automatically from the files already present in `data/`, so numbering continues correctly (`run01`, `run02`, `run03`, ...) for that driver even after closing and reopening the app. Switching to a different driver number starts that driver's run count from `01` independently.

Each workbook contains exactly four columns:

```text
Trial | Number | Response | Time
```

Example:

```text
1 | 7 | No Match | 17:30:01.125
2 | 3 | No Match | 17:30:03.375
3 | 3 | Match    | 17:30:05.625
```

No Correct Answer or Result column is stored.

## Installation

Windows is required because number audio uses Windows SAPI.

Open a terminal in the project folder:

```bash
py -m pip install -r requirements.txt
```

## Run

```bash
py -m streamlit run app.py
```

A browser window will open with the dashboard. Enter the driver number, then start the run.

## Important timing note

Windows SAPI speech is blocking: the program waits while the number is spoken. The code schedules stimulus onsets every 2.25 seconds and records the timestamp at stimulus onset.

Before collecting real experimental data, test the actual timing against the eye-tracker recording. For highly precise experimental timing, PsychoPy is generally preferable to Streamlit.

## Project structure

```text
n-back-driver-experiment/
├── data/
│   └── .gitkeep
├── src/
│   ├── data_manager.py
│   └── nback_task.py
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

## GitHub

The generated Excel files in `data/` are ignored by `.gitignore`, so participant data will not accidentally be committed to GitHub. Only `data/.gitkeep` is tracked, which keeps the empty folder present in the repository.
