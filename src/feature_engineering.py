import logging
import pandas as pd

logger = logging.getLogger(__name__)

class MiningFeatureEngineer:
    """Engineers domain specific KPIs and operational metrics for the haul truck telemetry data"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def engineer_all_features(self) -> pd.DataFrame:
        """Executes the full feature engineering pipeline sequentially."""
        logger.info("Initiating mining feature engineering pipeline...")

        self.compute_specific_fuel_consumption()
        self.compute_idling_ratio()
        self.compute_speed_consistency()
        self.calculate_operator_risk_profiles()

        logger.info("Feature engineering completed successfully.")
        return self.df
    
    def compute_specific_fuel_consumption(self):
        """Calculates Specific Fuel Consumption (SFC) in Litres per Tonne-Kilometre"""
        import numpy as np
        tonne_km = self.df["Load_Tonnes"] * self.df["Distance_km"]
        sfc_series = self.df["Fuel_Litres"] / tonne_km
        self.df["Specific_Fuel_Consumption"] = sfc_series.replace([np.inf, -np.inf], np.nan).fillna(0.0)
        logger.info("Feature engineered: Specific_Fuel_Consumption (L / Tonne-km).")

    def compute_idling_ratio(self):
        """Calculates the percentage of total trip time spent idling."""
        total_trip_minutes = self.df["Trip_Hours"] * 60
        self.df["Idling_Ratio"]  = (
            self.df["Idle_Minutes"] / total_trip_minutes
        ).fillna(0.0)
        logger.info("Feature engineered: Idling_Ratio (% of trip spent stationary).")

    def compute_speed_consistency(self):
        """Caluates the Speed Consistency Index"""
        self.df["Speed_Consistency_Index"] = (
            self.df["Avg_Speed_kmh"] / self.df["Trip_Hours"]
        ).fillna(0.0)
        logger.info("Feature engineered: Speed_Consistency_Index")

    def calculate_operator_risk_profiles(self):
        """Engineers a composite baseline score ranking operator inefficiency"""
        op_burn = self.df.groupby("Operator_ID")["Fuel_Efficiency_km_per_L"].transform("mean")
        op_idle = self.df.groupby("Operator_ID")["Idling_Ratio"].transform("mean")
        self.df["Operator_Efficiency_Dviation"] = (op_idle - op_burn)
        logger.info("Feature engineered: Operator_Efficiency_Deviation matrix.")
