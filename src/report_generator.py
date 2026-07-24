import os
import logging
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

class FleetVisualizer:
    """Generates publication-quality charts and visual insights for fleet data."""

    def __init__(self, df: pd.DataFrame, output_dir: str = "visuals"):
        self.df = df.copy()
        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)

        self.PRIMARY_NAVY = "#1E293B"
        self.ACCENT_BLUE = "#3B82F6"
        self.WARN_AMBER = "#F59E0B"
        self.CRT_RED = "#EF4444"

        self._apply_global_styles()

    def _apply_global_styles(self):
        """Applies a nice look to all plots"""
        sns.set_theme(style="whitegrid", rc={
            "font.family": "sans-serif",
            "grid.alpha": 0.3,
            "grid.linestyle": "--",
            "axes.edgecolor": "#CBD5E1",
            "axes.linewidth": 1.0
        })
        plt.rcParams.update({
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 13,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
        })

    def generate_all_plots(self):
        """Runs the entire visualisation suite sequentially"""
        logger.info("Starting visualisation engine...")

        self.plot_operational_frontier()
        self.plot_operator_efficiency_rankings()
        self.plot_idling_decay_analysis()

        logger.info(f"All visualisations exported susccessfully to the '{self.output_dir}/' directory.")

    def plot_operational_frontier(self):
        """Creates a scatter plot showing the Payload vs. Fuel consumption color coded by Risk """
        fig, ax = plt.subplots(figsize=(9,6))

        colors = {0: self.PRIMARY_NAVY, 1: self.WARN_AMBER, 2: self.CRT_RED}
        labels = {0: "Normal Operation", 1: "Medium Risk Warning", 2: "High Risk Anomaly"}

        for risk_val, group in self.df.groupby("Risk_Score"):
            ax.scatter(
                group["Load_Tonnes"],
                group["Fuel_Litres"],
                c=colors[risk_val],
                label=labels[risk_val],
                alpha=0.7 if risk_val > 0 else 0.4,
                edgecolors="none",
                s=40 if risk_val > 0 else 25
            )

        ax.set_title("Operational Efficiency Frontier: Payload vs. Fuel Consumption", pad=15, weight="bold")
        ax.set_xlabel("Payload (Load_Tonnes)")
        ax.set_ylabel("Fuel Consumed (Fuel_Litres)")
        ax.legend(frameon=True, facecolor="#F8FAFC", edgecolor="none")
            
        plt.tight_layout()
        save_path = os.path.abspath(os.path.join(self.output_dir, "01_operational_frontier.png"))
        plt.savefig(save_path, dpi=300)
        plt.close()
        logger.info("Exported: 01_operational_frontier.png")

    def plot_operator_efficiency_rankings(self):
        """Generates a horizontal bar chart showing fuel efficiency deviation from fleet average"""
        fig, ax = plt.subplots(figsize=(10,6))

        op_means = self.df.groupby("Operator_ID")["Fuel_Efficiency_km_per_L"].mean()
        global_mean = self.df["Fuel_Efficiency_km_per_L"].mean()
        deviation = (op_means - global_mean).sort_values()

        filtered_dev = pd.concat([deviation.head(5), deviation.tail(5)])
        bar_colors = [self.CRT_RED if x < 0 else self.ACCENT_BLUE for x in filtered_dev.values]

        ax.barh(filtered_dev.index, filtered_dev.values, color=bar_colors, alpha=0.85, height=0.6)
        ax.axvline(0, color=self.PRIMARY_NAVY, linestyle='-', linewidth=1.2, alpha=0.7)

        ax.set_title("Operator Performance: Fuel Efficiency Variance From Fleet Average", pad=15, weight="bold")
        ax.set_xlabel("Efficiency Deviation (km/L)")
        ax.set_ylabel("Operator_ID")

        sns.despine(left=True, bottom=True)
        plt.tight_layout()
        save_path = os.path.abspath(os.path.join(self.output_dir,"O2_operator_deviations.png"))
        plt.savefig(save_path, dpi=300)
        plt.close()
        logger.info("Exported: 02_operator_deviations.png")

    def plot_idling_decay_analysis(self):
        """Creates a joint hexbin plot correlating high idling ratios with efficiency decay"""
        plt.figure(figsize=(8, 6))

        plot_df = self.df.copy()
        plot_df["Idling_Percentage"] = plot_df["Idling_Ratio"] * 100

        joint_grid = sns.jointplot(
            data=plot_df,
            x="Idling_Percentage",
            y="Fuel_Efficiency_km_per_L",
            kind="hex",
            cmap="Blues",
            gridsize=25,
            color=self.ACCENT_BLUE
        )

        joint_grid.fig.subplots_adjust(top=0.9)
        joint_grid.fig.suptitle("Fuel Efficiency Decay vs. Trip Idling Ratio", weight="bold", y=0.95)
        joint_grid.set_axis_labels("Trip Idling Time (% of total duration)", "Fuel Efficiency (km/L)")

        save_path = os.path.abspath(os.path.join(self.output_dir,"03_idling_efficiency_decay.png"))
        plt.savefig(save_path, dpi=300)
        plt.close()
        logger.info("Exported: 03_idling_efficiency_decay.png")
            