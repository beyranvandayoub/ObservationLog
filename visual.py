# visual.py
# Astronomy Observation Log - Plots (Session 14 & 20)

def _get_df(data):
    try:
        import pandas as pd
        if hasattr(data, "to_dataframe"):
            return data.to_dataframe()
        elif isinstance(data, list):
            return pd.DataFrame([x.to_dict() if hasattr(x, "to_dict") else x for x in data])
        elif isinstance(data, pd.DataFrame):
            return data
    except ImportError:
        pass
    return None


def plot_exposure_by_target(data, save_path=None):
    try:
        import matplotlib.pyplot as plt
        df = _get_df(data)
        if df is None or df.empty:
            print("No data available to plot.")
            return

        grouped = df.groupby("target")["exposure"].sum() / 60
        plt.figure(figsize=(7, 4))
        plt.bar(grouped.index, grouped.values, color="steelblue")
        plt.title("Total Exposure Time by Target")
        plt.xlabel("Target")
        plt.ylabel("Exposure Time (minutes)")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print("Saved plot to:", save_path)
        plt.show()
    except ImportError:
        print("Please install matplotlib and pandas: pip install matplotlib pandas")


def plot_filter_distribution(data, save_path=None):
    try:
        import matplotlib.pyplot as plt
        df = _get_df(data)
        if df is None or df.empty:
            print("No data available to plot.")
            return

        filt_counts = df["filter_name"].value_counts()
        plt.figure(figsize=(6, 5))
        plt.pie(filt_counts.values, labels=filt_counts.index, autopct="%1.1f%%", startangle=90)
        plt.title("Filter Usage Distribution")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print("Saved plot to:", save_path)
        plt.show()
    except ImportError:
        print("Please install matplotlib and pandas: pip install matplotlib pandas")


def plot_observer_contributions(data, save_path=None):
    try:
        import matplotlib.pyplot as plt
        df = _get_df(data)
        if df is None or df.empty:
            print("No data available to plot.")
            return

        obs_exp = df.groupby("observer")["exposure"].sum() / 60
        plt.figure(figsize=(7, 4))
        plt.barh(obs_exp.index, obs_exp.values, color="seagreen")
        plt.title("Observer Total Exposure Time")
        plt.xlabel("Minutes")
        plt.ylabel("Observer")
        plt.grid(axis="x", linestyle="--", alpha=0.7)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print("Saved plot to:", save_path)
        plt.show()
    except ImportError:
        print("Please install matplotlib and pandas: pip install matplotlib pandas")


def plot_dashboard(data, save_path="observation_dashboard.png"):
    try:
        import matplotlib.pyplot as plt
        df = _get_df(data)
        if df is None or df.empty:
            print("No data available to plot.")
            return

        fig, axs = plt.subplots(2, 2, figsize=(10, 8))
        fig.suptitle("Astronomical Observation Log Dashboard")

        # 1. Target Exposure
        target_exp = df.groupby("target")["exposure"].sum() / 60
        axs[0, 0].bar(target_exp.index, target_exp.values, color="steelblue")
        axs[0, 0].set_title("Exposure by Target (min)")
        axs[0, 0].set_xlabel("Target")
        axs[0, 0].set_ylabel("Minutes")

        # 2. Filters
        filt_counts = df["filter_name"].value_counts()
        axs[0, 1].pie(filt_counts.values, labels=filt_counts.index, autopct="%1.0f%%")
        axs[0, 1].set_title("Filter Distribution")

        # 3. Observers
        obs_exp = df.groupby("observer")["exposure"].sum() / 60
        axs[1, 0].barh(obs_exp.index, obs_exp.values, color="seagreen")
        axs[1, 0].set_title("Observer Exposure (min)")
        axs[1, 0].set_xlabel("Minutes")

        # 4. Observation Type
        type_counts = df["obs_type"].value_counts()
        axs[1, 1].bar(type_counts.index, type_counts.values, color="purple")
        axs[1, 1].set_title("Observation Types")
        axs[1, 1].set_ylabel("Count")

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
            print("Dashboard saved to:", save_path)
        plt.show()
    except ImportError:
        print("Please install matplotlib and pandas: pip install matplotlib pandas")
