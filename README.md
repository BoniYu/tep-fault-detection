# Tennessee Eastman Process — Fault Detection

ML portfolio project: classify process faults in the Tennessee Eastman
Process (TEP), a well-known chemical process benchmark from Downs &
Vogel (1993). Combines chemical engineering domain knowledge with
applied ML — playing to a process-safety/industrial niche.

## Dataset

- Classic Chiang/Russell/Braatz small dataset (downloaded from
  web.mit.edu/braatzgroup).
- 22 scenarios: fault 0 = normal operation, faults 1–21 = distinct
  process faults (e.g. feed composition step changes, sticking valves,
  slow drift in reaction kinetics).
- Train files (d00.dat–d21.dat): fault present for the entire run.
- Test files (d00_te.dat–d21_te.dat): fault introduced partway through
  (sample 160 of 960) — the first part of each faulty test run is still
  normal operation.
- 52 variables per row: XMEAS_1–41 (process measurements) +
  XMV_1–11 (manipulated variables). Note: XMV_12 (agitator speed) is
  excluded in this dataset version, since it's held constant.
- Known quirk: `d00.dat` is stored transposed (52, 500) vs. every other
  file (n_samples, 52) — handled automatically in `data_loader.py`.

## Future Work

 An LSTM approach was explored on the `lstm-experiment` branch as a learning exercise; 
 it underperformed the XGBoost model on this dataset (see LSTM_REPORT.md on that branch for full analysis)


## Setup (for future reference)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cd src
python verify_data.py
```

## Reference

Downs, J.J. and Vogel, E.F. (1993). "A plant-wide industrial process
control problem." *Computers & Chemical Engineering*, 17(3), 245-255.
https://doi.org/10.1016/0098-1354(93)80018-I

Chiang, L.H., Russell, E.L., and Braatz, R.D. (2001). *Fault Detection
and Diagnosis in Industrial Systems*. Springer-Verlag London.
(Source of the classic small TEP dataset used here, and of the
commonly cited observation that faults 3, 9, and 15 are statistically
difficult to detect in this data — verified independently in this
project's own EDA.)

**Download source**: http://web.mit.edu/braatzgroup/TE_process.zip
(hosted by the Braatz Research Group, MIT). Not included in this repo —
see Setup instructions above for where to place the files after
downloading.