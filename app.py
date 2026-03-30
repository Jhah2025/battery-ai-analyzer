import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.loader import load_battery_data
from utils.segmentation import (
    segment_operating_mode,
    segment_power_level,
    summarize_segments,
)
from utils.features import (
    extract_basic_features,
    generate_summary_text,
)
from utils.plotting import (
    plot_core_timeseries,
    plot_mode_segmentation,
    plot_power_segmentation,
    plot_ecm_fit,
)
from utils.ecm import fit_1rc_constant_ocv, fit_2rc_constant_ocv


st.set_page_config(page_title="Battery AI Analyzer V2", layout="wide")

st.title("Battery AI Analyzer V2")
st.write(
    "Upload a battery test CSV file to visualize time-series behavior, "
    "segment operating modes, analyze power levels, and fit 1RC / 2RC ECMs."
)

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

with st.sidebar:
    st.header("Settings")

    current_rest_threshold_a = st.number_input(
        "Rest threshold current |I| <= (A)",
        min_value=0.0,
        value=0.05,
        step=0.01,
        format="%.3f",
    )

    use_manual_power_threshold = st.checkbox("Use manual power threshold", value=False)

    if use_manual_power_threshold:
        power_threshold_w = st.number_input(
            "High-power threshold |P| >= (W)",
            min_value=0.0,
            value=1.0,
            step=0.1,
            format="%.3f",
        )
        power_quantile = None
    else:
        power_quantile = st.slider(
            "Auto threshold quantile for |P|",
            min_value=0.1,
            max_value=0.95,
            value=0.7,
            step=0.05,
        )
        power_threshold_w = None

if uploaded_file is not None:
    try:
        # -------------------------
        # Load data
        # -------------------------
        df = load_battery_data(uploaded_file)

        st.subheader("1. Data Preview")
        st.dataframe(df.head(20), use_container_width=True)

        # -------------------------
        # Segmentation
        # -------------------------
        df = segment_operating_mode(
            df,
            current_rest_threshold_a=current_rest_threshold_a,
        )

        df = segment_power_level(
            df,
            abs_power_threshold_w=power_threshold_w,
            quantile=power_quantile if power_quantile is not None else 0.7,
        )

        mode_segments = summarize_segments(df, "mode")
        power_segments = summarize_segments(df, "power_level")

        # -------------------------
        # Basic features
        # -------------------------
        features = extract_basic_features(df)

        st.subheader("2. Basic Features")
        feature_df = pd.DataFrame(
            {"Metric": list(features.keys()), "Value": list(features.values())}
        )
        st.dataframe(feature_df, use_container_width=True)

        # -------------------------
        # Core plots
        # -------------------------
        st.subheader("3. Core Time-Series Plots")
        fig_core = plot_core_timeseries(df)
        st.pyplot(fig_core)

        # -------------------------
        # Mode segmentation
        # -------------------------
        st.subheader("4. Charge / Discharge / Rest Segmentation")
        fig_mode = plot_mode_segmentation(df)
        st.pyplot(fig_mode)

        st.write("Mode Segment Summary")
        st.dataframe(mode_segments, use_container_width=True)

        # -------------------------
        # Power segmentation
        # -------------------------
        st.subheader("5. Power Analysis and High / Low Power Segmentation")
        fig_power = plot_power_segmentation(df)
        st.pyplot(fig_power)

        st.write("Power Segment Summary")
        st.dataframe(power_segments, use_container_width=True)

        # -------------------------
        # Summary text
        # -------------------------
        st.subheader("6. Auto Summary")
        summary = generate_summary_text(features, mode_segments, power_segments)
        st.write(summary)

        # -------------------------
        # ECM fitting
        # -------------------------
        st.subheader("7. ECM Fitting: 1RC with Constant OCV")
        fit_1rc = fit_1rc_constant_ocv(df)

        col1, col2 = st.columns(2)
        with col1:
            st.write("1RC Parameters")
            st.json(fit_1rc["params"])
        with col2:
            st.metric("1RC RMSE (V)", f'{fit_1rc["rmse_v"]:.6f}')
            st.write(f"Success: {fit_1rc['success']}")
            st.write(f"Message: {fit_1rc['message']}")

        fig_1rc = plot_ecm_fit(
            df["time_min"].values,
            df["voltage_v"].values,
            fit_1rc["voltage_fit"],
            title="1RC ECM Fit",
            fitted_label="1RC Fit",
        )
        st.pyplot(fig_1rc)

        st.subheader("8. ECM Fitting: 2RC with Constant OCV")
        fit_2rc = fit_2rc_constant_ocv(df)

        col3, col4 = st.columns(2)
        with col3:
            st.write("2RC Parameters")
            st.json(fit_2rc["params"])
        with col4:
            st.metric("2RC RMSE (V)", f'{fit_2rc["rmse_v"]:.6f}')
            st.write(f"Success: {fit_2rc['success']}")
            st.write(f"Message: {fit_2rc['message']}")

        fig_2rc = plot_ecm_fit(
            df["time_min"].values,
            df["voltage_v"].values,
            fit_2rc["voltage_fit"],
            title="2RC ECM Fit",
            fitted_label="2RC Fit",
        )
        st.pyplot(fig_2rc)

        # -------------------------
        # Compare fit quality
        # -------------------------
        st.subheader("9. Fit Comparison")
        compare_df = pd.DataFrame(
            {
                "Model": ["1RC", "2RC"],
                "RMSE (V)": [fit_1rc["rmse_v"], fit_2rc["rmse_v"]],
            }
        )
        st.dataframe(compare_df, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading or analyzing file: {e}")
else:
    st.info("Please upload a CSV file to begin.")