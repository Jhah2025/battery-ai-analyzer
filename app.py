import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.loader import load_battery_data
from utils.features import extract_basic_features, generate_summary_text
from utils.plotting import plot_timeseries

st.set_page_config(page_title="Battery AI Analyzer", layout="wide")

st.title("Battery Test AI Analyzer")
st.write("Upload a battery test CSV file to visualize data and generate a quick engineering summary.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = load_battery_data(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df.head(20), use_container_width=True)

        st.subheader("Basic Features")
        features = extract_basic_features(df)
        feature_df = pd.DataFrame(
            {"Metric": list(features.keys()), "Value": list(features.values())}
        )
        st.dataframe(feature_df, use_container_width=True)

        st.subheader("Plots")
        fig = plot_timeseries(df)
        st.pyplot(fig)

        st.subheader("Auto Summary")
        summary = generate_summary_text(features)
        st.write(summary)

    except Exception as e:
        st.error(f"Error loading or analyzing file: {e}")
else:
    st.info("Please upload a CSV file to begin.")