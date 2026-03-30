import matplotlib.pyplot as plt


def _shade_segments(ax, df, label_col, color_map, alpha=0.18):
    values = df[label_col].values
    start_idx = 0

    for i in range(1, len(values)):
        if values[i] != values[i - 1]:
            label = values[start_idx]
            x0 = df["time_min"].iloc[start_idx]
            x1 = df["time_min"].iloc[i - 1]
            ax.axvspan(x0, x1, alpha=alpha, color=color_map.get(label, "gray"))
            start_idx = i

    label = values[start_idx]
    x0 = df["time_min"].iloc[start_idx]
    x1 = df["time_min"].iloc[-1]
    ax.axvspan(x0, x1, alpha=alpha, color=color_map.get(label, "gray"))


def plot_core_timeseries(df):
    fig, axes = plt.subplots(5, 1, figsize=(11, 15), sharex=True)

    axes[0].plot(df["time_min"], df["voltage_v"])
    axes[0].set_ylabel("Voltage (V)")
    axes[0].set_title("Voltage vs Time")
    axes[0].grid(True)

    axes[1].plot(df["time_min"], df["current_a"])
    axes[1].set_ylabel("Current (A)")
    axes[1].set_title("Current vs Time")
    axes[1].grid(True)

    axes[2].plot(df["time_min"], df["capacity_mah"])
    axes[2].set_ylabel("Capacity (mAh)")
    axes[2].set_title("Capacity vs Time")
    axes[2].grid(True)

    axes[3].plot(df["time_min"], df["soc"])
    axes[3].set_ylabel("SOC")
    axes[3].set_title("SOC vs Time")
    axes[3].grid(True)

    axes[4].plot(df["time_min"], df["power_w"])
    axes[4].set_ylabel("Power (W)")
    axes[4].set_xlabel("Time (min)")
    axes[4].set_title("Power vs Time")
    axes[4].grid(True)

    plt.tight_layout()
    return fig


def plot_mode_segmentation(df):
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    mode_color_map = {
        "charge": "tab:green",
        "discharge": "tab:red",
        "rest": "tab:blue",
    }

    axes[0].plot(df["time_min"], df["current_a"])
    _shade_segments(axes[0], df, "mode", mode_color_map)
    axes[0].set_ylabel("Current (A)")
    axes[0].set_title("Operating Mode Segmentation on Current")
    axes[0].grid(True)

    axes[1].plot(df["time_min"], df["voltage_v"])
    _shade_segments(axes[1], df, "mode", mode_color_map)
    axes[1].set_ylabel("Voltage (V)")
    axes[1].set_xlabel("Time (min)")
    axes[1].set_title("Operating Mode Segmentation on Voltage")
    axes[1].grid(True)

    plt.tight_layout()
    return fig


def plot_power_segmentation(df):
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    power_color_map = {
        "rest_power": "tab:blue",
        "low_power": "gold",
        "high_power": "tab:red",
    }

    axes[0].plot(df["time_min"], df["power_w"])
    _shade_segments(axes[0], df, "power_level", power_color_map)
    axes[0].set_ylabel("Power (W)")
    axes[0].set_title("Power vs Time with Power-Level Segmentation")
    axes[0].grid(True)

    axes[1].plot(df["time_min"], df["abs_power_w"])
    _shade_segments(axes[1], df, "power_level", power_color_map)
    axes[1].set_ylabel("|Power| (W)")
    axes[1].set_xlabel("Time (min)")
    axes[1].set_title("Absolute Power vs Time")
    axes[1].grid(True)

    plt.tight_layout()
    return fig


def plot_ecm_fit(time_min, voltage_measured, voltage_fit, title="ECM Fit", fitted_label="Fit"):
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.plot(time_min, voltage_measured, label="Measured Voltage")
    ax.plot(time_min, voltage_fit, label=fitted_label)
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title(title)
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    return fig