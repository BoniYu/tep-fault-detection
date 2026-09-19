"""This script loads data from a path and has functions to load data from a path
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Number of variables in the dataset
N_VARS = 52  # 41 measurements + 11 manipulated variables = 52 columns
XMEAS = [f"XMEAS_{i}" for i in range(1, 42)]  # Number of measurements
XMV = [f"XMV_{i}" for i in range(1, 12)]  # Number of manipulated variables
COLUMN_NAMES = XMEAS + XMV  # Column names for the dataset

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

def load_fault_set(fault_number, split):
    """Load one fault's data (0-21) as a labeled DataFrame.
    split must be 'train' or 'test'."""
    suffix = "_te" if split == "test" else ""
    fname = f"d{fault_number:02d}{suffix}.dat"
    path = DATA_DIR / fname

    arr = np.loadtxt(path)

    # d00.dat (normal training set) is stored sideways vs every other file
    if arr.shape[1] != N_VARS and arr.shape[0] == N_VARS:
        arr = arr.T

    df = pd.DataFrame(arr, columns=COLUMN_NAMES)
    df.insert(0, "faultNumber", fault_number)
    return df

def load_all():
    """Load every fault (0-21) for both train and test, each as one
    big combined DataFrame."""
    train_frames = [load_fault_set(f, "train") for f in range(22)]
    test_frames = [load_fault_set(f, "test") for f in range(22)]
    return pd.concat(train_frames, ignore_index=True), pd.concat(test_frames, ignore_index=True)

