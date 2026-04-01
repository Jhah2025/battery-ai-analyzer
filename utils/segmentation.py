import numpy as np
import pandas as pd


def segment_operating_mode(df: pd.DataFrame, current_rest_threshold_a: float = 0.05):
    mode = np.where(
        df["current_a"].abs() <= current_rest_threshold_a,
        "rest",
        np.where(df["current_a"] < 0, "discharge", "charge"),
    )
    out = df.copy()
    out["mode"] = mode
    return out


def segment_power_level(
    df: pd.DataFrame,
    abs_power_threshold_w: float | None = None,
    quantile: float = 0.7,
):
    out = df.copy()
    abs_power = out["power_w"].abs()

    if abs_power_threshold_w is None:
        abs_power_threshold_w = abs_power.quantile(quantile)

    labels = np.where(
        abs_power < 1e-8,
        "rest_power",
        np.where(abs_power >= abs_power_threshold_w, "high_power", "low_power"),
    )

    out["power_level"] = labels
    return out