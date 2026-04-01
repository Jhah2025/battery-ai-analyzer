import streamlit as st
import pandas as pd

from utils.loader import load_battery_data
from utils.segmentation import segment_operating_mode, segment_power_level
from utils.features import extract_basic_features
from utils.plotting import plot_core_timeseries
from utils.ecm import fit_1rc_constant_ocv, fit_2rc_constant_ocv
from utils.retrieval import load_text_file, simple_retrieve
from utils.agent import answer_user_question
from utils.report import build_analysis_package


st.set_page_config(page_title="Battery AI Copilot", layout="wide")

st.title("Battery AI Copilot - Phase C")
st.write(
    "Upload battery test data and a requirement document, then ask engineering questions."
)

csv_file = st.file_uploader("Upload battery CSV", type=["csv"])
txt_file = st.file_uploader("Upload requirement TXT", type=["txt"])

user_question = st.text_input(
    "Ask a question",
    value="Does this test violate the voltage requirement?",
)

if csv_file is not None:
    df = load_battery_data(csv_file)
    df = segment_operating_mode(df, current_rest_threshold_a=0.05)
    df = segment_power_level(df, abs_power_threshold_w=None, quantile=0.7)

    features = extract_basic_features(df)
    fit_1rc = fit_1rc_constant_ocv(df)
    fit_2rc = fit_2rc_constant_ocv(df)

    st.subheader("Battery Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("Core Plots")
    fig = plot_core_timeseries(df)
    st.pyplot(fig)

    st.subheader("Basic Features")
    feature_df = pd.DataFrame(
        {"Metric": list(features.keys()), "Value": list(features.values())}
    )
    st.dataframe(feature_df, use_container_width=True)

    st.subheader("ECM Fit Summary")
    ecm_df = pd.DataFrame(
        {
            "Model": ["1RC", "2RC"],
            "RMSE (V)": [fit_1rc["rmse_v"], fit_2rc["rmse_v"]],
        }
    )
    st.dataframe(ecm_df, use_container_width=True)

    requirement_text = ""
    retrieved_chunks = []

    if txt_file is not None:
        requirement_text = load_text_file(txt_file)
        retrieved_chunks = simple_retrieve(user_question, requirement_text, top_k=3)

        st.subheader("Retrieved Requirement Context")
        for i, chunk in enumerate(retrieved_chunks, start=1):
            st.markdown(f"**Chunk {i}:** {chunk}")

    analysis_package = build_analysis_package(
        features=features,
        fit_1rc=fit_1rc,
        fit_2rc=fit_2rc,
    )

    if st.button("Run Copilot"):
        answer = answer_user_question(
            question=user_question,
            analysis_package=analysis_package,
            retrieved_contexts=retrieved_chunks,
        )

        st.subheader("Copilot Answer")
        st.write(answer)

else:
    st.info("Please upload a battery CSV to begin.")