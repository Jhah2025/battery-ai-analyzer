import pandas as pd


def load_battery_data(file) -> pd.DataFrame:
    """
    Load battery CSV data and normalize column names.
    Expected columns from your CSV:
        time_cali_s
        Ecell_V
        I_mA
        QDischarge_cali_mA_h
        SOC
    """

    df = pd.read_csv(file)

    required_columns = [
        "time_cali_s",
        "Ecell_V",
        "I_mA",
        "QDischarge_cali_mA_h",
        "SOC",
    ]

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.rename(
        columns={
            "time_cali_s": "time_s",
            "Ecell_V": "voltage_v",
            "I_mA": "current_ma",
            "QDischarge_cali_mA_h": "capacity_mah",
            "SOC": "soc",
        }
    )

    numeric_cols = ["time_s", "voltage_v", "current_ma", "capacity_mah", "soc"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols).reset_index(drop=True)

    df["time_min"] = df["time_s"] / 60.0
    df["current_a"] = df["current_ma"] / 1000.0

    # Raw electrical power at the terminal
    df["power_w"] = df["voltage_v"] * df["current_a"]
    df["abs_power_w"] = df["power_w"].abs()

    # Model-friendly discharge-positive current
    # raw current is negative during discharge in your file
    df["i_discharge_a"] = -df["current_a"]

    dt = df["time_s"].diff().fillna(0.0)
    if len(dt) > 1:
        dt.iloc[0] = dt.iloc[1]
    df["dt_s"] = dt

    return df