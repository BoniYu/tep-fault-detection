import streamlit as st
import pandas as pd
import joblib
import sys

sys.path.append("src")
from variable_reference import describe_column

st.title("TEP Fault Detection")
st.write("Pick a fault type to load a real example, then adjust the "
         "top variables to see how the model's prediction changes.")

model = joblib.load("models/xgb_trend_model.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")
feature_columns = joblib.load("models/feature_columns.pkl")

st.write("Model loaded successfully.")
st.write(f"Expects {len(feature_columns)} input features.")