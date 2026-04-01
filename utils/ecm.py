import numpy as np
from scipy.optimize import least_squares


def simulate_1rc_constant_ocv(time_s, current_a_raw, params):
    Uoc, R0, R1, C1 = params

    i = -np.asarray(current_a_raw, dtype=float)
    t = np.asarray(time_s, dtype=float)

    n = len(t)
    i1 = np.zeros(n)
    tau1 = max(R1 * C1, 1e-12)

    for k in range(1, n):
        dt = t[k] - t[k - 1]
        di1 = (i[k - 1] - i1[k - 1]) / tau1
        i1[k] = i1[k - 1] + dt * di1

    v = Uoc - i * R0 - i1 * R1
    return v


def simulate_2rc_constant_ocv(time_s, current_a_raw, params):
    Uoc, R0, R1, C1, R2, C2 = params

    i = -np.asarray(current_a_raw, dtype=float)
    t = np.asarray(time_s, dtype=float)

    n = len(t)
    i1 = np.zeros(n)
    i2 = np.zeros(n)

    tau1 = max(R1 * C1, 1e-12)
    tau2 = max(R2 * C2, 1e-12)

    for k in range(1, n):
        dt = t[k] - t[k - 1]
        di1 = (i[k - 1] - i1[k - 1]) / tau1
        di2 = (i[k - 1] - i2[k - 1]) / tau2
        i1[k] = i1[k - 1] + dt * di1
        i2[k] = i2[k - 1] + dt * di2

    v = Uoc - i * R0 - i1 * R1 - i2 * R2
    return v


def fit_1rc_constant_ocv(df):
    time_s = df["time_s"].values
    current_a = df["current_a"].values
    voltage_v = df["voltage_v"].values

    p0 = [4.0, 0.02, 0.2, 10000.0]
    lb = [2.5, 1e-5, 1e-5, 1.0]
    ub = [5.0, 0.5, 2.0, 1e7]

    def residuals(p):
        return simulate_1rc_constant_ocv(time_s, current_a, p) - voltage_v

    result = least_squares(residuals, p0, bounds=(lb, ub))
    v_fit = simulate_1rc_constant_ocv(time_s, current_a, result.x)

    return {
        "params": {
            "Uoc_V": float(result.x[0]),
            "R0_ohm": float(result.x[1]),
            "R1_ohm": float(result.x[2]),
            "C1_F": float(result.x[3]),
            "tau1_s": float(result.x[2] * result.x[3]),
        },
        "voltage_fit": v_fit,
        "rmse_v": float(np.sqrt(np.mean((v_fit - voltage_v) ** 2))),
        "success": bool(result.success),
        "message": result.message,
    }


def fit_2rc_constant_ocv(df):
    time_s = df["time_s"].values
    current_a = df["current_a"].values
    voltage_v = df["voltage_v"].values

    p0 = [4.0, 0.02, 0.02, 500.0, 0.10, 5000.0]
    lb = [2.5, 1e-5, 1e-5, 1.0, 1e-5, 1.0]
    ub = [5.0, 0.5, 2.0, 1e7, 2.0, 1e8]

    def residuals(p):
        return simulate_2rc_constant_ocv(time_s, current_a, p) - voltage_v

    result = least_squares(residuals, p0, bounds=(lb, ub))
    v_fit = simulate_2rc_constant_ocv(time_s, current_a, result.x)

    return {
        "params": {
            "Uoc_V": float(result.x[0]),
            "R0_ohm": float(result.x[1]),
            "R1_ohm": float(result.x[2]),
            "C1_F": float(result.x[3]),
            "tau1_s": float(result.x[2] * result.x[3]),
            "R2_ohm": float(result.x[4]),
            "C2_F": float(result.x[5]),
            "tau2_s": float(result.x[4] * result.x[5]),
        },
        "voltage_fit": v_fit,
        "rmse_v": float(np.sqrt(np.mean((v_fit - voltage_v) ** 2))),
        "success": bool(result.success),
        "message": result.message,
    }