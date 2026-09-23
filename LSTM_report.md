# LSTM Experiment — Findings Report

## Motivation

Tree-based models (Random Forest, XGBoost) plateaued on faults 10 and
13 despite filtering, tuning, and trend/rate-of-change features (see
main REPORT.md). This branch tests whether an LSTM, which can learn
directly from raw sequences rather than engineered snapshot features,
can succeed where those approaches couldn't.

## Setup

- Data reshaped into sliding windows (window=20 timesteps = 1 hour of
  history, step=1) via `build_sequences()`, built separately per fault
  run to avoid sequences crossing between different faults
- 52 raw variables used (no PCA reduction, no manual trend features —
  the LSTM is expected to learn temporal patterns itself)
- Faults 3, 9, 15 excluded, consistent with the tree-based models
- Standardized features (StandardScaler), required for neural networks
  unlike tree-based models

## Issues encountered

**Validation split bug**: Keras's `validation_split` doesn't shuffle
data, so with fault-ordered sequences it produced a validation set
made almost entirely of the last few fault classes. Fixed with a
proper stratified `train_test_split` before training. See notebook
for details.
## Results

### Validation performance (properly split, no leakage)

After fixing an initial data leakage bug (overlapping windows split
randomly rather than by time), honest validation accuracy landed in
the 76-80% range across several runs, using early stopping
(patience=3) to halt training once validation stopped improving.
Neural network training is sensitive to random initialization
(unlike tree-based models), so results vary run-to-run even with
identical settings — a real property of this approach worth noting,
not a bug.

### Test evaluation issues discovered

Raw test accuracy: 58.0% — but this number is misleading. Diagnosed
by checking accuracy separately on pre-fault windows (samples 1-140,
still genuinely normal operation despite being labeled with a fault
number) vs. genuinely faulty windows (samples >160):

- Pre-fault windows: 5.5% accuracy (expected — the model is correctly
  NOT predicting the fault, since the data genuinely looks normal;
  it's being graded against an intentionally wrong label)
- Genuinely faulty windows: 68.6% accuracy — a more honest estimate

**Second issue identified**: applying `fix_test_labels()` (used
successfully for the tree-based models) before building sequences
creates a new leakage problem specific to sequence data — relabeled
rows from different original fault runs get grouped together under
the same `faultNumber=0` label, and sliding windows can span the
boundary between two physically unrelated simulation runs, producing
fabricated, non-physical sequences. Fix in progress: track original
run identity separately from (corrected) label, and skip windows that
straddle a label change.

**Takeaway**: label correction that worked cleanly for row-independent
tree models introduces new complexity for sequence models, since
windows have to respect true run boundaries, not just row-level
labels.


## Comparison to tree-based models

*(to be added)*

## Conclusion

*(to be added)*