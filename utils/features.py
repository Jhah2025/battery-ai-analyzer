import pandas as pd


def extract_basic_features(df: pd.DataFrame):
    duration_s = df["time_s"].iloc[-1] - df["time_s"].iloc[0]
    duration_min = duration_s / 60.0

    voltage_max = df["voltage_v"].max()
    voltage_min = df["voltage_v"].min()
    voltage_mean = df["voltage_v"].mean()

    current_max_a = df["current_a"].max()
    current_min_a = df["current_a"].min()
    current_mean_a = df["current_a"].mean()

    power_max_w = df["power_w"].max()
    power_min_w = df["power_w"].min()
    abs_power_max_w = df["abs_power_w"].max()
    abs_power_mean_w = df["abs_power_w"].mean()

    capacity_end_mah = df["capacity_mah"].iloc[-1]

    soc_start = df["soc"].iloc[0]
    soc_end = df["soc"].iloc[-1]
    soc_drop = soc_start - soc_end

    features = {
        "Duration (min)": round(duration_min, 3),
        "Max Voltage (V)": round(voltage_max, 5),
        "Min Voltage (V)": round(voltage_min, 5),
        "Mean Voltage (V)": round(voltage_mean, 5),
        "Max Current (A)": round(current_max_a, 5),
        "Min Current (A)": round(current_min_a, 5),
        "Mean Current (A)": round(current_mean_a, 5),
        "Max Power (W)": round(power_max_w, 5),
        "Min Power (W)": round(power_min_w, 5),
        "Max |Power| (W)": round(abs_power_max_w, 5),
        "Mean |Power| (W)": round(abs_power_mean_w, 5),
        "End Capacity (mAh)": round(capacity_end_mah, 5),
        "Start SOC": round(soc_start, 5),
        "End SOC": round(soc_end, 5),
        "SOC Drop": round(soc_drop, 5),
    }

    return features


def _segment_duration_summary(segment_df: pd.DataFrame):
    if segment_df.empty:
        return {}

    duration_by_label = segment_df.groupby("label")["duration_s"].sum().to_dict()
    return {k: round(v, 3) for k, v in duration_by_label.items()}


def generate_summary_text(features, mode_segments, power_segments):
    duration = features["Duration (min)"]
    vmin = features["Min Voltage (V)"]
    vmax = features["Max Voltage (V)"]
    imean = features["Mean Current (A)"]
    pabs_max = features["Max |Power| (W)"]
    soc_start = features["Start SOC"]
    soc_end = features["End SOC"]

    mode_duration = _segment_duration_summary(mode_segments)
    power_duration = _segment_duration_summary(power_segments)

    if imean < 0:
        dominant_behavior = "discharge-dominant"
    elif imean > 0:
        dominant_behavior = "charge-dominant"
    else:
        dominant_behavior = "near-zero-current"

    text = (
        f"This test lasted {duration:.2f} minutes. "
        f"The cell voltage ranged from {vmin:.3f} V to {vmax:.3f} V. "
        f"The mean current was {imean:.3f} A, indicating a predominantly {dominant_behavior} profile. "
        f"The maximum absolute terminal power was {pabs_max:.3f} W. "
        f"SOC changed from {soc_start:.3f} to {soc_end:.3f}. "
    )

    if mode_duration:
        text += f"Operating-mode durations (s) were approximately: {mode_duration}. "

    if power_duration:
        text += f"Power-level durations (s) were approximately: {power_duration}. "

    text += (
        "This workflow provides a first-pass engineering view of battery behavior, "
        "including operating-mode segmentation, power characterization, and dynamic ECM fitting."
    )

    return text