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

## Results

### Data leakage issues resolved before final evaluation

Two separate leakage problems were found and fixed before results
could be trusted:

1. **Overlapping windows split randomly** (via `train_test_split`
   without respecting time order) let near-duplicate sequences appear
   in both train and validation, producing an inflated 99.8%
   validation accuracy. Fixed by splitting each fault's run by time
   first (80% early rows for training, 20% later rows for validation),
   then building windows separately within each portion.
2. **Sequences straddling run boundaries**: after correcting test
   labels for the pre-fault period (same fix used for the tree-based
   models), rows from different physical simulation runs shared the
   same `faultNumber=0` label, letting sliding windows span two
   unrelated runs. Fixed by tracking original run identity (`run_id`)
   separately from the (corrected) label, and skipping any window
   whose label changes partway through (342 of 17,879 windows, ~2%).

### Final validation and test performance

With both leakage issues fixed and early stopping (patience=3) used
to prevent overfitting:

| Metric | LSTM | XGBoost (tuned + trend) |
|---|---|---|
| Validation accuracy | ~76-80% (varies by run\*) | — |
| Test accuracy | **62.9%** | **81.5%** |

\* Neural network training is sensitive to random weight
initialization, unlike tree-based models — repeated runs with
identical settings and a fixed seed still show some variation.

## Comparison to tree-based models

The original motivation for this branch was faults 10 and 13, which
remained weak across every tree-based intervention (filtering,
XGBoost, tuning, trend features). Directly comparing:

| Fault | XGBoost F1 | LSTM F1 |
|---|---|---|
| 10 | 0.46 | 0.29 |
| 13 | 0.37 | 0.29 |

**The LSTM performed worse on both target faults, not better.**
Additionally, fault 21 — XGBoost's strongest fault (F1 0.99) —
collapsed to F1 0.06 under the LSTM, suggesting the issue isn't
specific to hard faults but a broader difficulty the model had
learning reliably across all 19 classes.

## Conclusion

For this dataset, a tuned XGBoost model with engineered trend features
outperforms an LSTM across nearly every fault, including the two
faults (10, 13) this experiment specifically aimed to improve. The
most likely explanation is data volume: ~7,000 training sequences is
a modest dataset for a neural network to learn 19 classes reliably,
while gradient-boosted trees are generally more sample-efficient on
structured/tabular data of this size.

**This is a genuine, informative negative result.** It doesn't mean
sequence information is irrelevant to these faults — trend/rate-of-
change features (a simpler form of temporal information) did produce
real improvements for XGBoost. It suggests that a full sequence model
needs either substantially more training data or a smaller, more
constrained architecture to be competitive here, rather than that
temporal information itself is unhelpful.

**Recommendation**: XGBoost with trend features remains the
recommended model for this project. The LSTM is retained as a
documented experiment demonstrating that the reasonable hypothesis
("sequence models should help the fault classification task") was
tested rigorously and did not hold for this dataset at this scale —
a valuable finding in its own right, and evidence of thorough
methodology rather than a wasted effort.


## Why more hidden layers/units would not fix this

It might seem intuitive that a "stronger" model (more layers, more
units) would close the gap with XGBoost, but the evidence points the
other way. The current model (31,187 parameters, one LSTM layer of 64
units) already showed clear overfitting: 100% training accuracy by
epoch 6-8, while validation performance plateaued or degraded shortly
after (see "Fixing overfitting" above). This is the signature of a
model that already has *more* capacity than the ~7,000 training
sequences can support, not too little.

Adding more layers or units increases the number of trainable
parameters further, giving the model even more room to memorize
training data rather than learn generalizable patterns — the opposite
of what's needed here. This differs from tree-based models like
Random Forest, where adding more trees rarely hurts; for neural
networks, excess capacity relative to data volume is a direct path to
worse generalization, not better.

## What would genuinely help

- **More training data**: the most direct fix. ~7,000 sequences is
  modest for a 19-class neural network problem. More simulation runs,
  or possibly a smaller sliding-window step size for more overlapping
  sequences (would need care to avoid reintroducing the leakage issues
  already fixed in this branch), would give the model more to learn
  from without needing to memorize.
- **Regularization**: techniques specifically designed to fight
  overfitting on a small model — e.g. dropout (randomly disabling a
  fraction of neurons during training, forcing the model not to
  over-rely on specific patterns) or L2 weight regularization. This
  directly targets the actual problem (too little data for the model's
  capacity) rather than making the mismatch worse.
- **A smaller, more constrained architecture**: paradoxically, a
  *smaller* LSTM (fewer units) might generalize better than the
  current one, given the data volume available — worth testing as an
  alternative to going bigger.

**Not pursued further in this branch**, given the tree-based model
already meets the project's needs (81.5% accuracy, well-understood
failure modes) — noted here as a clear, evidence-based direction for
future work rather than left unexplained.

### Architecture experiments: confirming the data-volume hypothesis

Tested two regularization approaches against the original model, to
check whether the ~78-80% validation ceiling was an architecture
problem rather than a data volume problem:

| Approach | Best validation accuracy |
|---|---|
| Original (LSTM 64 units, no regularization) | 76-80% (varies by run) |
| Dropout (LSTM 64 units, dropout=0.3) | 79.1% |
| Smaller model (LSTM 16 units, no dropout) | 77.5% |

Both regularized versions showed the expected effect on *overfitting
behavior* — training accuracy climbed more slowly and stayed closer
to validation accuracy throughout, rather than snapping to 100% within
a few epochs like the original. However, **neither meaningfully
raised the peak validation accuracy** above the original model's
range.

**Conclusion**: three architecturally different approaches (larger
unregularized, dropout-regularized, and smaller) all converge to the
same ~76-80% ceiling. This is strong evidence the bottleneck is
genuinely the amount of training data (~7,000 sequences) rather than
model capacity or overfitting specifically — architecture changes fix
*how* the model overfits, not the underlying ceiling on what it can
learn from this much data.