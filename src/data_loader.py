import os
import logging
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)

class HaulTruckDataLoader:
    """Handles ingestion, schema validation and type casting for haul truck telemetry data."""

    EXPECTED_SCHEMA = {
        "Date": "datetime64[ns]",
        "Truck_ID": "object",
        "Operator_ID": "object",
        "Route": "object",
        "Distance_km": "float64",
        "Fuel_Litres": "float64",
        "Idle_Minutes": "float64",
        "Load_Tonnes": "float64",
        "Trip_Hours": "float64",
        "Avg_Speed_kmh": "float64",
        "Fuel_Efficiency_km_per_L": "float64",
        "Expected_Anomaly": "int64"
    }

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None

    def load_data(self) -> pd.DataFrame:
        """Loads the raw CSV dataset into a Pandas DataFrame with validation checks."""
        if not os.path.exists(self.file_path):
            logger.error(f"Data ingestion failed: File not found at {self.file_path}")
            raise FileNotFoundError(f"Target data file missing: {self.file_path}")

        logger.info(f"Initiating ingestion pipeline for: {self.file_path}")

        #Read file
        self.df = pd.read_csv(self.file_path)
        logger.info(f"Raw data successfully read. Shape: {self.df.shape} rows, {self.df.shape} columns.")

        #Run quality validations
        self._validate_columns()
        self._enforce_data_types()
        self._check_missing_values()

        logger.info("Ingestion pipeline completed sucessfully.")
        return self.df
    

    def _validate_columns(self):
        """Validates that all expected structural columns are present in the source file."""
        missing_cols = [col for col in self.EXPECTED_SCHEMA if col not in self.df.columns]
        if missing_cols:
            logger.error(f"Schema Validation Failure: Missing expected columns: {missing_cols}")
            raise ValueError(f"Dataset structural mismatch. Missing field: {missing_cols}")
        logger.info("Schema structural verification: PASSED.")

    def _enforce_data_types(self):
        """Enforces explicit casting of object types, metrics and temporal fields."""
        try:
            self.df["Date"] = pd.to_datetime(self.df["Date"])
            for col, dtype in self.EXPECTED_SCHEMA.items():
                if col != "Date":
                    self.df[col] = self.df[col].astype(dtype)
            logger.info("Data type enforcement and schem casting: PASSED.")
        except Exception as e:
            logger.error(f"Data type transformation failure: {str(e)}")
            raise TypeError(f"Ingested data failed production type-casting rules: {e}")

    def _check_missing_values(self):
        """Scans for unexpected nulls within the pipeline dataset."""
        null_counts = self.df.isnull().sum()
        total_nulls = null_counts.sum()

        if total_nulls > 0:
            logger.warning(f"Data Quality Warning: Detected {total_nulls} missing entries.")
        else:
            logger.info("Data Integrity check: 0 null values encountered.")

