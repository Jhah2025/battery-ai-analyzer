import pandas as pd


def load_battery_data(file) -> pd.DataFrame:
    """
    Load battery CSV data and normalize column names for downstream analysis.
    Expected original columns in your CSV:
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

    # Rename to simpler internal names
    df = df.rename(
        columns={
            "time_cali_s": "time_s",
            "Ecell_V": "voltage_v",
            "I_mA": "current_ma",
            "QDischarge_cali_mA_h": "capacity_mah",
            "SOC": "soc",
        }
    )

    # Ensure numeric
    numeric_cols = ["time_s", "voltage_v", "current_ma", "capacity_mah", "soc"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=numeric_cols).reset_index(drop=True)

    # Add convenient converted columns
    df["time_min"] = df["time_s"] / 60.0
    df["current_a"] = df["current_ma"] / 1000.0

    return df