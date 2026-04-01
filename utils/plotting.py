import matplotlib.pyplot as plt


def plot_core_timeseries(df):
    fig, axes = plt.subplots(5, 1, figsize=(10, 14), sharex=True)

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