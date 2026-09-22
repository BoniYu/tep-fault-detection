import streamlit as st
import pandas as pd
import joblib
import sys

sys.path.append("src")
from variable_reference import describe_column
from fault_reference import describe

st.title("TEP Fault Detection")
st.write("Adjust the key process variables below and see the model's "
         "fault prediction update in real time.")

model = joblib.load("models/xgb_trend_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")
app_config = joblib.load("models/app_config.pkl")
variable_ranges = app_config["variable_ranges"]
pair_relationships = app_config["pair_relationships"]
baseline_row = app_config["baseline_row"]
baseline_full = app_config["baseline_full"]
top_10_variables = app_config["top_10_variables"]

st.subheader("Adjust key variables")

if st.button("Reset to baseline"):
    for var in top_10_variables:
        st.session_state[var] = baseline_row[var]

st.subheader("Adjust key variables")

user_values = {}
for var in top_10_variables:
    low, high = variable_ranges[var]
    default = baseline_row[var]
    user_values[var] = st.slider(
        describe_column(var),
        min_value=float(low),
        max_value=float(high),
        value=float(default),
        key=var
    )

user_values = {}
for var in top_10_variables:
    low, high = variable_ranges[var]
    default = baseline_row[var]
    user_values[var] = st.slider(
        describe_column(var),
        min_value=float(low),
        max_value=float(high),
        value=float(default)
    )


def build_full_input(user_values, baseline_row, baseline_full, pair_relationships, feature_columns):
    current = dict(baseline_full)
    changed_vars = set(user_values.keys())

    for var, value in user_values.items():
        current[var] = value

    for dependent, (independent, slope, intercept) in pair_relationships.items():
        if independent in user_values:
            current[dependent] = slope * current[independent] + intercept
            changed_vars.add(dependent)

    for var in changed_vars:
        current[f"{var}_change"] = current[var] - baseline_row[var]
        current[f"{var}_rolling"] = (4 * baseline_row[var] + current[var]) / 5

    return current


full_input = build_full_input(user_values, baseline_row, baseline_full, pair_relationships, feature_columns)




input_df = pd.DataFrame([full_input])[feature_columns]

prediction_encoded = model.predict(input_df)[0]
prediction = label_encoder.inverse_transform([prediction_encoded])[0]

probabilities = model.predict_proba(input_df)[0]
confidence = probabilities[prediction_encoded]

st.subheader("Prediction")
st.write(f"**{describe(prediction)}**")
st.write(f"Confidence: {confidence:.1%}")    