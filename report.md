# TEP Fault Detection — Findings Report

## Dataset

Classic Chiang/Russell/Braatz small TEP dataset: 22 scenarios (normal +
21 faults), 52 process variables per sample. See README.md for full
dataset details and citations.

## EDA Findings

### Fault signatures can hide in unexpected places

Fault 4 (reactor cooling water inlet temperature step) shows almost no
visible change in reactor temperature itself (XMEAS_9) — the process's
own control loop compensates for the disturbance. The fault's actual
signature appears instead in the reactor cooling water flow valve
(XMV_10), which shows a clear, sustained shift after the fault begins.

**Implication**: a "directly affected" variable can look deceptively
normal if a control loop is compensating for it. Supports using all 52
variables for classification rather than hand-picking "obvious" ones
per fault.

### Faults 3, 9, and 15 are visually indistinguishable from normal operation

Confirmed independently (via direct plotting against normal operation)
the commonly cited claim (Chiang, Russell & Braatz, 2001) that these
three faults produce no visible shift in this dataset. Plan: train
models both with and without these faults to quantify the actual
impact.


## Correlation Analysis

Checked pairwise correlation across all 52 variables during normal
operation, to see which move together.

**12 pairs found above 0.85 correlation.** Nearly all of them are a
control valve (XMV) paired with the exact measurement (XMEAS) it
directly regulates — e.g. the separator liquid valve (XMV_7) with
separator level (XMEAS_12), or the A feed valve (XMV_3) with A feed
rate (XMEAS_1). A few are physically connected downstream units, like
reactor/separator/stripper pressure all correlating with each other,
since pressure changes propagate through the connected process train.

**Takeaway**: these correlations reflect the plant's real control
architecture, not noise or redundant data — a good sanity check that
the simulation behaves physically. Not a concern for the tree-based
models (Random Forest/XGBoost) we're using first, since they handle
correlated features fine.

### Correlation structure reflects the plant's real control architecture

12 variable pairs show correlation above 0.85 during normal operation,
almost entirely valve/measurement pairs (e.g. XMV_7 separator valve
with XMEAS_12 separator level) or physically connected downstream units
(reactor/separator/stripper pressure). This is a sanity check that the
simulated process behaves physically, not a data quality concern.



## Modeling

*(to be added)*

## Conclusions

*(to be added)*