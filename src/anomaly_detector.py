import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

logger = logging.getLogger(__name__)

class HaulTruckAnomalyDetector:
    """Detects the fleet fuel inefficiencies using statistical Z-scores and Isolation Forest  ML"""

    def __init__(self, df: pd.DataFrame, contamination_rate: float = 0.02):
        self.df = df.copy()
        self.contamination_rate = contamination_rate
        self.ml_features = [
            "Fuel_Litres",
            "Distance_km",
            "Idle_Minutes",
            "Specific_Fuel_Consumption",
            'Idling_Ratio'
        ]

    def run_detection_pipeline(self) -> pd.DataFrame:
        """Executes statistical and machine learning anomaly detection models"""
        logger.info("Starting anomaly detection engine...")

        self.detect_route_zscore_anomalies()
        self.detect_isolation_forest_anomalies()
        self.compute_consensus_risk_score()

        logger.info("Anomaly detection completed successfully")
        return self.df

    def detect_route_zscore_anomalies(self):
        """Calculates Fuel Efficiency Z-Scores grouped by route to manage terrain variations"""
        logger.info("Computing localised Z-scores per mining route...")

        route_stats = self.df.groupby("Route")["Fuel_Efficiency_km_per_L"]
        mean_mapped = route_stats.transform("mean")
        std_mapped = route_stats.transform("std")

        self.df["Route_Fuel_ZScore"] = (self.df["Fuel_Efficiency_km_per_L"] - mean_mapped) / std_mapped.replace(0, np.ma)
        self.df["Route_Fuel_ZScore"] = self.df["Route_Fuel_ZScore"].fillna(0.0)

        self.df["ZScore_Anomaly"] = (self.df["Route_Fuel_ZScore"] < -3.0).astype(int)

        total_z_anomalies = self.df["ZScore_Anomaly"].sum()
        logger.info(f" -> Statistical Z-Score complete. Flagged {total_z_anomalies} localised trips.")

    def detect_isolation_forest_anomalies(self):
        """Trains an Isolation Forest model to detect complec multi-variable anomalies"""
        logger.info(f"Training Isolation Forest model(Contamination rate: {self.contamination_rate})...")

        iso_forest = IsolationForest(
            contamination=self.contamination_rate,
            random_state=42,
            n_jobs=-1
        )

        predictions = iso_forest.fit_predict(self.df[self.ml_features])
        self.df["IForest_Anomaly"] = np.where(predictions == -1, 1, 0)

        total_ml_anomalies = self.df["IForest_Anomaly"].sum()
        logger.info(f" -> Isolation Forest complete. Flagged {total_ml_anomalies} multi-variable trips.")

    def compute_consensus_risk_score(self):
        """Builds a consesus engine cross models to calculate an asset Risk_Score."""
        self.df["Risk_Score"] = self.df["ZScore_Anomaly"] + self.df["IForest_Anomaly"]
        high_risk_count = (self.df["Risk_Score"] == 2).sum()
        logger.info(f" -> Consensus Engine calculated. Confirmed {high_risk_count} HIGH-RISK operational assets.")
        