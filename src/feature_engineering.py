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