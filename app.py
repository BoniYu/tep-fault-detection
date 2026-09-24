import streamlit as st
import pandas as pd
import joblib
import sys
import streamlit.components.v1 as components

sys.path.append("src")
from variable_reference import describe_column
from fault_reference import describe, FAULT_DESCRIPTIONS

st.title("TEP Fault Detection")
st.write("Adjust the key process variables below and see the model's "
         "fault prediction update in real time.")

with st.expander("What do the fault types mean?"):
    for fault_num in sorted(FAULT_DESCRIPTIONS.keys()):
        st.write(f"**{describe(fault_num)}**")

model = joblib.load("models/xgb_trend_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")
app_config = joblib.load("models/app_config.pkl")
variable_ranges = app_config["variable_ranges"]
pair_relationships = app_config["pair_relationships"]
baseline_row = app_config["baseline_row"]
baseline_full = app_config["baseline_full"]
top_10_variables = app_config["top_10_variables"]


def build_process_diagram(user_values, baseline_row, top_10_variables):
    def color_for(var):
        return "#e74c3c" if abs(user_values[var] - baseline_row[var]) > 1e-6 else "#2c3e50"

    def weight_for(var):
        return "bold" if abs(user_values[var] - baseline_row[var]) > 1e-6 else "normal"

    svg = f"""
    <svg viewBox="0 0 900 420" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">
      <style>
        .box {{ fill: #ecf0f1; stroke: #34495e; stroke-width: 2; }}
        .label {{ font-family: sans-serif; font-size: 13px; }}
        .arrow {{ stroke: #7f8c8d; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }}
      </style>
      <defs>
        <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" fill="#7f8c8d"/>
        </marker>
      </defs>

      <rect class="box" x="20" y="160" width="110" height="70"/>
      <text x="75" y="200" class="label" text-anchor="middle">Feed</text>

      <rect class="box" x="200" y="160" width="130" height="90"/>
      <text x="265" y="210" class="label" text-anchor="middle">Reactor</text>

      <rect class="box" x="400" y="30" width="110" height="60"/>
      <text x="455" y="65" class="label" text-anchor="middle">Compressor</text>

      <rect class="box" x="400" y="160" width="110" height="70"/>
      <text x="455" y="200" class="label" text-anchor="middle">Separator</text>

      <rect class="box" x="580" y="160" width="110" height="70"/>
      <text x="635" y="200" class="label" text-anchor="middle">Stripper</text>

      <text x="820" y="200" class="label" text-anchor="middle">Product</text>

      <path class="arrow" d="M130,195 H200"/>
      <path class="arrow" d="M330,195 H400"/>
      <path class="arrow" d="M455,160 V90"/>
      <path class="arrow" d="M400,60 H265 V160"/>
      <path class="arrow" d="M510,195 H580"/>
      <path class="arrow" d="M690,195 H770"/>

      <text x="75" y="245" class="label" fill="{color_for('XMV_3')}" font-weight="{weight_for('XMV_3')}" text-anchor="middle">{describe_column('XMV_3')}</text>
      <text x="75" y="262" class="label" fill="{color_for('XMV_4')}" font-weight="{weight_for('XMV_4')}" text-anchor="middle">{describe_column('XMV_4')}</text>
      <text x="75" y="279" class="label" fill="{color_for('XMEAS_1')}" font-weight="{weight_for('XMEAS_1')}" text-anchor="middle">{describe_column('XMEAS_1')}</text>

      <text x="265" y="275" class="label" fill="{color_for('XMV_10')}" font-weight="{weight_for('XMV_10')}" text-anchor="middle">{describe_column('XMV_10')}</text>
      <text x="265" y="292" class="label" fill="{color_for('XMEAS_9')}" font-weight="{weight_for('XMEAS_9')}" text-anchor="middle">{describe_column('XMEAS_9')}</text>
      <text x="265" y="309" class="label" fill="{color_for('XMEAS_21')}" font-weight="{weight_for('XMEAS_21')}" text-anchor="middle">{describe_column('XMEAS_21')}</text>

      <text x="455" y="110" class="label" fill="{color_for('XMV_5')}" font-weight="{weight_for('XMV_5')}" text-anchor="middle">{describe_column('XMV_5')}</text>

      <text x="635" y="245" class="label" fill="{color_for('XMV_9')}" font-weight="{weight_for('XMV_9')}" text-anchor="middle">{describe_column('XMV_9')}</text>
      <text x="635" y="262" class="label" fill="{color_for('XMEAS_18')}" font-weight="{weight_for('XMEAS_18')}" text-anchor="middle">{describe_column('XMEAS_18')}</text>
      <text x="635" y="279" class="label" fill="{color_for('XMEAS_19')}" font-weight="{weight_for('XMEAS_19')}" text-anchor="middle">{describe_column('XMEAS_19')}</text>
    </svg>
    """
    return svg


st.subheader("Process flow")
diagram_placeholder = st.empty()

if st.button("Reset to baseline"):
    for var in top_10_variables:
        st.session_state[var] = baseline_row[var]

st.subheader("Adjust key variables")

user_values = {}
col1, col2 = st.columns(2)
half = len(top_10_variables) // 2

with col1:
    for var in top_10_variables[:half]:
        low, high = variable_ranges[var]
        default = baseline_row[var]
        user_values[var] = st.slider(
            describe_column(var),
            min_value=float(low),
            max_value=float(high),
            value=float(default),
            key=var
        )

with col2:
    for var in top_10_variables[half:]:
        low, high = variable_ranges[var]
        default = baseline_row[var]
        user_values[var] = st.slider(
            describe_column(var),
            min_value=float(low),
            max_value=float(high),
            value=float(default),
            key=var
        )

with diagram_placeholder.container():
    diagram_svg = build_process_diagram(user_values, baseline_row, top_10_variables)
    components.html(diagram_svg, height=440)


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