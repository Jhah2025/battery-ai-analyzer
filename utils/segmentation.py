import numpy as np
import pandas as pd


def segment_operating_mode(df: pd.DataFrame, current_rest_threshold_a: float = 0.05):
    """
    Segment into charge / discharge / rest based on current.
    Raw convention:
      current_a < 0 -> discharge
      current_a > 0 -> charge
    """

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
    """
    Segment into rest_power / low_power / high_power.
    Uses absolute terminal power magnitude.
    """

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
    out["abs_power_w"] = abs_power
    return out


def summarize_segments(df: pd.DataFrame, column: str):
    """
    Summarize contiguous segments for a categorical column.
    Example columns:
      - mode
      - power_level
    """

    values = df[column].values
    start_idx = 0
    segments = []

    for i in range(1, len(values)):
        if values[i] != values[i - 1]:
            segments.append(
                {
                    "label": values[start_idx],
                    "start_index": start_idx,
                    "end_index": i - 1,
                    "start_time_s": float(df["time_s"].iloc[start_idx]),
                    "end_time_s": float(df["time_s"].iloc[i - 1]),
                    "duration_s": float(df["time_s"].iloc[i - 1] - df["time_s"].iloc[start_idx]),
                }
            )
            start_idx = i

    segments.append(
        {
            "label": values[start_idx],
            "start_index": start_idx,
            "end_index": len(values) - 1,
            "start_time_s": float(df["time_s"].iloc[start_idx]),
            "end_time_s": float(df["time_s"].iloc[-1]),
            "duration_s": float(df["time_s"].iloc[-1] - df["time_s"].iloc[start_idx]),
        }
    )

    return pd.DataFrame(segments)