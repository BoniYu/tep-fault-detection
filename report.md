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

## PCA analysis
### Effective dimensionality is much lower than 52 variables

PCA on all 52 variables (normal + faulty training data) shows strong
diminishing returns: 11 components capture 80% of total variance, 18
components capture 90%, and 22 capture 95%. This aligns with the
correlation findings above — many variables are redundant with each
other (valve positions strongly tracking the measurements they
control), so the process's true degrees of freedom are meaningfully
lower than the raw variable count.

**Implication**: dimensionality reduction (e.g. reducing to ~18 PCA
components) is a reasonable option for the LSTM model later, where
fewer input dimensions can reduce overfitting risk. Not necessary for
tree-based models (Random Forest/XGBoost), which handle
high-dimensional, correlated features natively.


## EDA Findings after full EDA

### Overview

Explored the classic Chiang/Russell/Braatz TEP dataset (22 scenarios:
normal + 21 faults, 52 process variables per sample) to understand the
data's structure and behavior before any modeling. No missing values
found in either the training or test sets.

### 1. Fault signatures can hide in unexpected places

Fault 4 (reactor cooling water inlet temperature step) shows almost no
visible change in reactor temperature itself (XMEAS_9) when plotted
against normal operation — the process's own control loop compensates
for the disturbance in real time. The fault's actual signature instead
appears in the reactor cooling water flow valve (XMV_10), which shows
a clear, sustained shift once the fault begins (test data, fault
introduced at sample 160).

**Implication**: a variable directly named in a fault's description
isn't necessarily where that fault is most visible — well-controlled
processes can mask disturbances in the "obvious" variable while
revealing them in the variable actively compensating for it. Supports
using all 52 variables for classification, not just fault-specific
ones chosen by intuition.

### 2. Faults 3, 9, and 15 are visually indistinguishable from normal operation

Directly plotted these three faults against normal operation and
confirmed they show no visible shift — independently verifying the
commonly cited claim from Chiang, Russell & Braatz (2001) that these
faults are statistically undetectable in this dataset's noise level.

**Decision**: rather than excluding these faults outright (standard
practice in much of the literature), plan to train models both with
and without them included, to directly measure and report the actual
impact — a more rigorous approach than assuming the literature's
finding applies unchanged to this specific modeling pipeline.

### 3. Correlation structure reflects the plant's real control architecture

Pairwise correlation across all 52 variables (normal operation only)
found 12 variable pairs above 0.85 correlation. Nearly all are a
control valve (XMV) paired with the exact measurement (XMEAS) it
directly regulates — e.g. the separator liquid valve (XMV_7) perfectly
correlated (1.000) with separator level (XMEAS_12), or the A feed
valve (XMV_3) with A feed rate (XMEAS_1, 0.996). A few reflect
physically connected downstream units, like reactor, separator, and
stripper pressure all correlating with each other as pressure changes
propagate through the connected process train.

**Implication**: these correlations reflect the plant's genuine
control architecture, not noise or data quality issues — a good sanity
check that the simulation behaves physically. Not a concern for the
tree-based models used first (Random Forest/XGBoost), which handle
correlated features natively.

### 4. Faults show uneven separability under PCA

A 2D PCA projection (6 representative faults, standardized data,
training set) showed Fault 6 (A feed loss) forming a clearly separated
cluster, while Normal operation, Fault 4, and Fault 14 overlapped
almost entirely in the same central region. Faults 1 and 13 partially
separated but with meaningful overlap.

**Implication**: not all faults will be equally easy to classify.
Faults like 6, with large, distinct effects on the process, should be
straightforward; faults like 4 and 14, whose effects are subtler or
compensated for by control loops, will likely be harder to distinguish
from normal operation — expect this to show up later in the model's
confusion matrix.

### 5. Effective dimensionality is much lower than 52 variables

Full PCA (all components, standardized training data) shows strong
diminishing returns: 11 components capture 80% of total variance, 18
components capture 90%, and 22 capture 95%. This lines up with the
correlation findings above — many variables are redundant with each
other, so the process's true degrees of freedom are meaningfully lower
than the raw 52-variable count suggests.

**Implication**: dimensionality reduction (e.g. ~18 PCA components) is
a reasonable option to explore for the LSTM stretch goal later, where
fewer, less-correlated input dimensions can reduce overfitting risk.
Not necessary for the tree-based baseline models, which handle
high-dimensional, correlated features natively.

### Summary of decisions carried into modeling

- Use all 52 raw variables for Random Forest/XGBoost (no scaling or
  dimensionality reduction needed for tree-based models)
- Train and compare models with and without faults 3, 9, 15 included
- Expect uneven per-fault performance; use confusion matrix (not just
  overall accuracy) to evaluate
- Consider PCA-reduced features specifically for the LSTM stretch goal

### Note on the 160-sample fault injection point

The original Downs & Vogel (1993) paper defines the process simulator
and the 20 faults, but does not specify a train/test split or a fixed
fault injection point — it only recommends 24-48h simulation runs to
observe full effects. The convention used in this dataset (test runs:
960 samples/48h, fault introduced at sample 160/8h) comes from how the
Chiang/Russell/Braatz dataset itself was generated, not from the
original paper. Confirmed empirically in EDA (visual inspection +
deviation-based onset detection across all 21 faulty test runs).



## Modeling

### Baseline: Random Forest

Trained a Random Forest (100 trees) on two dataset variants, per the
plan from EDA: all 22 fault classes, and excluding faults 3/9/15.

| Metric | All faults | Excluding 3/9/15 |
|---|---|---|
| Overall accuracy | 58.4% | 70.9% |
| Normal (0) recall | 0.32 | 0.62 |
| Normal (0) precision | 0.70 | 0.83 |

**Faults 3, 9, 15 confirmed undetectable by the model** (F1-scores
0.12-0.14 in the full model) — consistent with EDA findings.

**Root cause of Normal's poor performance identified**: confusion
matrix analysis showed 74% of all Normal misclassifications were
specifically confused with faults 3, 9, and 15 — not spread evenly
across faults. Removing these three faults nearly doubled Normal's
recall (0.32 -> 0.62), confirming they were actively degrading
performance on other classes, not just failing on their own.

**Strong performers** (F1 > 0.90): faults 1, 2, 4, 6, 7, 14, 17 — with
fault 4 notably strong (0.94) despite its effect being invisible in
the "obviously affected" variable (XMEAS_9), confirming the EDA
finding that its signature lives in the compensating control variable
(XMV_10) instead.

**Remaining weak performers** even after filtering: faults 10, 16, 20,
and Normal itself (F1 0.3-0.5) — worth investigating further, possibly
via a full confusion matrix, before concluding the model is complete.

## Conclusions

*(to be added)*