import os
import sys
import logging
from src.config_loader import PipelineConfig
from src.data_loader import HaulTruckDataLoader
from src.feature_engineering import MiningFeatureEngineer
from src.anomaly_detector import HaulTruckAnomalyDetector
from src.report_generator import FleetVisualizer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline_execution.log", mode="w")
    ]
)
logger= logging.getLogger(__name__)

def generate_terminal_executive_summary(df, fuel_cost_rate):
    """Parses pipeline outputs to print an operational summary to the terminal"""
    total_trips = len(df)
    total_fuel = df["Fuel_Litres"].sum()
    total_idle_hours = df["Idle_Minutes"].sum() / 60

    high_risk_trips = (df["Risk_Score"] == 2).sum()
    med_risk_trips = (df["Risk_Score"] == 1).sum()

    estimated_fuel_cost = total_fuel * fuel_cost_rate
    avg_idle_ratio = df["Idling_Ratio"].mean() * 100

    top_idlers = df.groupby("Operator_ID")["Idling_Ratio"].mean().sort_values(ascending=False).head(3)
    bad_trucks =df.groupby("Truck_ID")["Specific_Fuel_Consumption"].mean().sort_values(ascending=False).head(3)

    print("\n" + "="*72)
    print("     EXECUTIVE FLEET EFFICIENCY REPORT - PIPELINE RUN SUCCESSFUL     ")
    print("="*72)
    print(f"[+] Fleet Scope Monitored        : {total_trips:,} Active Haul Truck Trips")
    print(f"[+] Total Fuel Consumption       : {total_fuel:,.2f} Litres (~${estimated_fuel_cost:,.2f} USD)")
    print(f"[+] Fleet Idling Burden          : {total_idle_hours:,.1f} Hours (Avg: {avg_idle_ratio:.1f}% per trip)")
    print("-"* 72)
    print("ADVANCED ANOMALY METRICS TRIGGERED:")
    print(f"    - HIGH-RISK INCIDENTS        : {high_risk_trips} trips (Statistical & ML Consensus)")
    print(f"    - MEDIUM-RISK WARNINGS       : {med_risk_trips} trips (Single Model Flag)")
    print("-"* 72)
    print("TARGETED ASSET MANAGEMENT RECOMMENDATIONS:")
    print("     1. High-Idling Operators (Target for Training Review):")
    for op, val in top_idlers.items():
        print(f"        - {op}: Spends  {val*100:.1f}% of trip duration stationary")
    print ("    2. Mechanical Outliers (Target for Maintenance Inspection):")
    for trk, val in bad_trucks.items():
        print(f"        - {trk}: High Burn Rate ({val:.4f} Litres/Tonne-km)")
    print("="*72 + "\n")


def main():
    """Orchestrates the entire end-to-end telemetry analytics pipeline"""
    print("SYSTEM CHECK: main() has successfully started!")
    logger.info("Initialising Fleet Efficiency Analytics Orchestrator...")

    try:
        config = PipelineConfig()

        loader = HaulTruckDataLoader(file_path=config.paths["input_data"])
        raw_df = loader.load_data()

        engineer = MiningFeatureEngineer(df=raw_df)
        engineered_df = engineer.engineer_all_features()

        detector = HaulTruckAnomalyDetector(
            df=engineered_df,
            contamination_rate=config.anomaly_settings["isolation_forest"]["contamination_rate"]
        )
        final_insights_df = detector.run_detection_pipeline()

        os.makedirs(os.path.dirname(config.paths["output_data"]), exist_ok=True)
        final_insights_df.to_csv(config.paths["output_data"], index=False)
        logger.info(f"Production output registry successfully compiled: {config.paths['output_data']}")

        visualizer = FleetVisualizer(df=final_insights_df, output_dir=config.paths["visuals_dir"])
        visualizer.generate_all_plots()

        generate_terminal_executive_summary(
            df=final_insights_df,
            fuel_cost_rate=config.financials["fuel_cost_per_litre_usd"]
        )

    except FileNotFoundError as fnf_err:
        logger.critical(f"Pipeline Interrupted - Input Data Source Missing: {fnf_err}")
        sys.exit(1)
    except Exception as exc:
        logger.critical(f"Critical System Failure Encountered During Runtime Execution: {exc}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
        main()
