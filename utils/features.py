def extract_basic_features(df):
    duration_s = df["time_s"].iloc[-1] - df["time_s"].iloc[0]
    duration_min = duration_s / 60.0

    features = {
        "Duration (min)": round(duration_min, 3),
        "Min Voltage (V)": round(df["voltage_v"].min(), 5),
        "Max Voltage (V)": round(df["voltage_v"].max(), 5),
        "Mean Voltage (V)": round(df["voltage_v"].mean(), 5),
        "Min Current (A)": round(df["current_a"].min(), 5),
        "Max Current (A)": round(df["current_a"].max(), 5),
        "Mean Current (A)": round(df["current_a"].mean(), 5),
        "Max |Power| (W)": round(df["abs_power_w"].max(), 5),
        "End Capacity (mAh)": round(df["capacity_mah"].iloc[-1], 5),
        "Start SOC": round(df["soc"].iloc[0], 5),
        "End SOC": round(df["soc"].iloc[-1], 5),
        "SOC Drop": round(df["soc"].iloc[0] - df["soc"].iloc[-1], 5),
    }
    return features