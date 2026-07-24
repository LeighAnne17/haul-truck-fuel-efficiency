import pytest
import pandas as pd
import numpy as np
from src.feature_engineering import MiningFeatureEngineer

@pytest.fixture
def sample_telemetry_data():
    """Generates a clean, preedictable mock telemetry dataset for unit testing"""
    data = {
        "Date": pd.to_datetime(["2025-01-01", "2025-01-02", "2025-01-03"]),
        "Truck_ID": ["TR001", "TR002", "TR003"],
        "Operator_ID": ["OP001", "OP002", "OP001"],
        "Route": ["North_Pit", "North_Pit", "South_Dump"],
        "Distance_km": [10.0, 20.0, 0.0],
        "Fuel_Litres": [50.0, 100.0, 10.0],
        "Idle_Minutes": [30.0, 0.0, 60.0],
        "Load_Tonnes": [200.0, 250.0, 0.0],
        "Trip_Hours": [1.0, 2.0, 1.0],
        "Avg_Speed_kmh": [40.0, 50.0, 0.0],
        "Fuel_Efficiency_km_per_L": [0.2, 0.2, 0.0],
        "Expected_Anomaly": [0, 0, 1]
    }
    return pd.DataFrame(data)

def test_specific_fuel_consumption_calculation(sample_telemetry_data):
    """Verifies that SFC handles standard calculations and avoids division by zero erroes"""
    engineer = MiningFeatureEngineer(sample_telemetry_data)
    processed_df = engineer.engineer_all_features()

    assert processed_df.loc[0, "Specific_Fuel_Consumption"] == 0.025

    assert processed_df.loc[2, "Specific_Fuel_Consumption"] == 0.0

def test_idling_ratio_calculation(sample_telemetry_data):
    """Verifies that the Idling Ratio computes the correct tempral percentage"""
    engineer = MiningFeatureEngineer(sample_telemetry_data)
    processed_df = engineer.engineer_all_features()

    assert processed_df.loc[0, "Idling_Ratio"] == 0.5

    assert processed_df.loc[1, "Idling_Ratio"] == 0.0