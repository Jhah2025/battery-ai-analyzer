def extract_basic_features(df):
    """
    Extract simple battery-test features for Version 0.
    """
    duration_s = df["time_s"].iloc[-1] - df["time_s"].iloc[0]
    duration_min = duration_s / 60.0

    voltage_max = df["voltage_v"].max()
    voltage_min = df["voltage_v"].min()
    voltage_mean = df["voltage_v"].mean()

    current_max_a = df["current_a"].max()
    current_min_a = df["current_a"].min()
    current_mean_a = df["current_a"].mean()

    capacity_end_mah = df["capacity_mah"].iloc[-1]

    soc_start = df["soc"].iloc[0]
    soc_end = df["soc"].iloc[-1]
    soc_drop = soc_start - soc_end

    features = {
        "Duration (min)": round(duration_min, 2),
        "Max Voltage (V)": round(voltage_max, 4),
        "Min Voltage (V)": round(voltage_min, 4),
        "Mean Voltage (V)": round(voltage_mean, 4),
        "Max Current (A)": round(current_max_a, 4),
        "Min Current (A)": round(current_min_a, 4),
        "Mean Current (A)": round(current_mean_a, 4),
        "End Capacity (mAh)": round(capacity_end_mah, 4),
        "Start SOC": round(soc_start, 4),
        "End SOC": round(soc_end, 4),
        "SOC Drop": round(soc_drop, 4),
    }

    return features


def generate_summary_text(features):
    """
    Generate a simple rule-based engineering summary.
    """
    duration = features["Duration (min)"]
    vmin = features["Min Voltage (V)"]
    vmax = features["Max Voltage (V)"]
    imean = features["Mean Current (A)"]
    cap = features["End Capacity (mAh)"]
    soc_start = features["Start SOC"]
    soc_end = features["End SOC"]
    soc_drop = features["SOC Drop"]

    current_behavior = "discharge" if imean < 0 else "charge"

    summary = (
        f"This test lasted {duration:.2f} minutes. "
        f"The cell voltage ranged from {vmin:.3f} V to {vmax:.3f} V. "
        f"The mean current was {imean:.3f} A, indicating predominantly {current_behavior} behavior. "
        f"The final recorded discharged capacity was {cap:.2f} mAh. "
        f"SOC changed from {soc_start:.3f} to {soc_end:.3f}, corresponding to a drop of {soc_drop:.3f}. "
        f"This Version 0 workflow provides a quick first-pass visualization and summary of the battery test."
    )

    return summary