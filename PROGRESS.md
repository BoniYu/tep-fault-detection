## Progress log

19/9/2026 — Project setup
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
- [ ] Baseline model (Random Forest): train and evaluate twice — once with all 20 faults, once excluding faults 3/9/15 — compare results
- [ ] Evaluate and iterate


19/9/2026 — EDA: initial exploration

- Switched to a Jupyter notebook (`notebooks/eda.ipynb`) for exploratory
  work, instead of a plain script
- Confirmed no missing values in train or test sets
- Built `src/variable_reference.py`: maps XMEAS/XMV column names to
  human-readable descriptions (e.g. XMV_10 = "Reactor cooling water
  flow valve"), pulled from the paper's Tables 3-5
- **Key finding — Fault 4 (reactor cooling water inlet temp step)**:
  - `XMEAS_9` (reactor temperature) barely shows any visible change
    after the fault starts (sample 160) — the control loop compensates
    for it successfully
  - `XMV_10` (reactor cooling water flow) shows a clear, sustained
    shift after sample 160 — this is where the fault's effect actually
    shows up, since the controller is actively adjusting this valve to
    counteract the disturbance
  - **Takeaway**: a fault can be "hidden" in the variable most
    obviously affected, while showing up clearly in the manipulated
    variable compensating for it. Supports using all 52 variables for
    classification, not just the "obvious" ones per fault
- Still to check: faults 3, 9, 15 (commonly flagged in literature as
  statistically undetectable in this dataset)