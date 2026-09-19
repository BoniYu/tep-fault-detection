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

## Progress log

**[today's date]** — Project setup
- Built project folder structure: `data/raw/`, `src/`, `notebooks/`
- Set up a Python virtual environment (`.venv`) with
  `requirements.txt` listing: numpy, pandas, scikit-learn, matplotlib,
  seaborn, jupyter
- Wrote `src/data_loader.py`:
  - `load_fault_set(fault_number, split)` — loads one file, auto-fixes
    the d00.dat transpose issue
  - `load_all()` — loads and combines all 44 files into train/test
    DataFrames
- Wrote `src/verify_data.py` to sanity-check the loader
- **Verified**: Train shape (10580, 53), Test shape (21120, 53), all
  22 faults present in both — matches expected row counts
  (500 + 21×480 = 10580 train; 22×960 = 21120 test)

## Next steps

- [ ] EDA: visually compare normal vs. faulty runs
- [ ] Check faults 3, 9, 15 for detectability (commonly excluded in
      literature — confirm before deciding)
- [ ] Decide feature engineering approach (raw values vs. rate-of-change
      vs. rolling stats)
- [ ] Baseline model (Random Forest or XGBoost)
- [ ] Evaluate and iterate

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