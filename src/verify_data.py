from data_loader import load_all

train, test = load_all()

print("Train shape:", train.shape)
print("Test shape:", test.shape)

print("\nFaults found in train:", sorted(train["faultNumber"].unique()))
print("Faults found in test:", sorted(test["faultNumber"].unique()))

print("\nFirst few rows of train:")
print(train.head())