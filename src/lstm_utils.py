"""
Utilities for reshaping the TEP dataset into sequences for an LSTM,
since LSTMs need (samples, timesteps, features) instead of the flat
(rows, features) shape used by Random Forest/XGBoost.
"""

import numpy as np


def build_sequences(df, feature_cols, window=20, step=1):
    """
    Slides a window of `window` consecutive rows across each fault's
    run separately (never crossing between different fault runs), to
    build overlapping sequences.

    Returns:
        X: array of shape (num_sequences, window, num_features)
        y: array of shape (num_sequences,) - the fault label for each sequence
    """
    X_sequences = []
    y_sequences = []

    for fault_num in sorted(df["faultNumber"].unique()):
        fault_data = df[df["faultNumber"] == fault_num][feature_cols].values

        for start in range(0, len(fault_data) - window + 1, step):
            window_data = fault_data[start:start + window]
            X_sequences.append(window_data)
            y_sequences.append(fault_num)

    return np.array(X_sequences), np.array(y_sequences)