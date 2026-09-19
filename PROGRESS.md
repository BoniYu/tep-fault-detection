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