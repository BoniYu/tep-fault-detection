"""
Feature engineering / label correction for the TEP dataset before
modeling.
"""

FAULT_INTRODUCED_AT_SAMPLE = 160  # test data only; faults start here


def fix_test_labels(test_df):
    df = test_df.copy()
    
    position_in_run = df.groupby("faultNumber").cumcount() + 1
    
    is_faulty_run = df["faultNumber"] != 0
    is_before_fault = position_in_run <= FAULT_INTRODUCED_AT_SAMPLE
    
    mislabeled = is_faulty_run & is_before_fault
    df.loc[mislabeled, "faultNumber"] = 0
    
    print(f"Relabeled {mislabeled.sum()} rows from faulty to normal "
          f"(pre-fault period in test data)")
    return df

def add_trend_features(df, columns, window=5):
    """
    Adds rate-of-change and rolling-average columns for the given
    variables, computed within each fault run separately (so trends
    never leak across different fault runs).
    """
    df = df.copy()

    for col in columns:
        df[f"{col}_change"] = df.groupby("faultNumber")[col].diff()
        df[f"{col}_rolling"] = (
            df.groupby("faultNumber")[col]
            .transform(lambda x: x.rolling(window, min_periods=1).mean())
        )

    # First row of each run has no "previous row" to diff against
    df = df.fillna(0)
    return df