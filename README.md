# Haul Truck Fuel Efficiency Analytics Pipeline
An end-to-end data analytics pipeline built with Python, Pandas and Sckit-learn to process haul truck telemetry data, engineer fleet performance metrics, detect anomalies as well as generate automated reports for fleet performance analysis.

---

## Project Overview
Haul trucks generate large amounts of telemetry ata during their daily mining operations, so analysing this typ pf data can help to identify inefficient fuel usage, excessive idling, operator performance issue and equipment that may need maintanance. This project processes raw telemetry data through a modular analytics pipeline that cleans and validates the data, engineers mining-specific performance metrics, detects anomalies using statistical and and machine learning technologies and also produces reports and visualizations for fleet analysis.

---

## Project Objectives
The pipeline was developed to:
- Clean and validate hul truck telemetry data
- Engineer meaningful fleet performance metrics
- Detect unsual fuel consumption and operating behaviour
- Generate automated reports and visualizations
- Export processed data for further analysis
  
---

## Technology Stack
- Python
- Pandas
- Numpy
- SciPy
- Scikit-learn
- Matplotlib
- PyYAML
- Pytest

----

## Pipeline Workflow
### 1. Data Loading & Validation
- Load project configuration settings
- Read the haul truck telemetry data
- Validate the required columns and data types
- Handle missing and invalid values before analyzing

### 2. Feature Engineering
The pipeline calcultes additional metrics so to better evaluate fleet performance, which are : 
  - Specific Fuel Consumption
  - Idling Ratio
  - Speed Consistency Index
  - Operator Efficiency Deviation
These metrics help provide a clearer picture of efficiency than the raw telemetry values alone.

### 3. Anomaly Detection
The pipeline combines statistical analysis with machine learning to identify unusual operating behaviour.
With the **Route Based Z-Score** fuel consumption is compared only with trips that take place in the same route so to reduce false positives caused by different haul conditions. And then **Isolation Forest** analyses multiple operational variables together so to identify patterns that are difficult to detect using statistical methods alone.
Trips flagged by both methods are considered higher rik anomalies for futher invetigation.

### 4. Report Generation
After the analysis, the pipeline authomatically:
- Generates a processed dataset
- Produces summary visualizations
- Displays an executive summary in the terminal
- Saves the execution logs

---
## Handling Edge Cases
Some maintanance records had zero payload or zero travel distance which produced division-by-zero errors during feture engineering and so to ensure that the pipeline remained stable the infinite values were converted to missing values before they were replaced wit valid defaults.

## Running the Project
Install the required packages:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python main.py
```

Run the tests:

```bash
python -m pytest tests/
```
---

## Pipeline Outputs
After a successful run, the pipeline generates:
- Processd telemetry dataset
- Fleet performance summary
- Executive terminal report
- Fleet visualizations
- Pipeline Execution log
---

## Visualizations
<img width="2700" height="1800" alt="01_operational_frontier" src="https://github.com/user-attachments/assets/06980ece-4635-482d-9aaf-9c856a272265" />

<img width="3000" height="1800" alt="O2_operator_deviations" src="https://github.com/user-attachments/assets/8dabb36c-0710-45d6-80c4-34730d785c9f" />

<img width="1800" height="1800" alt="03_idling_efficiency_decay" src="https://github.com/user-attachments/assets/b6c25b22-2b15-49d1-a785-19326ba44568" />


## Skills Demonstrated
- Data Cleaning
- Data Validation
- Feature Engineering
- Statistical Analysis
- Exploratory Data Analysis
- Anomaly Detection
- Machine Learning
- Object-Oriented Programming (OOP)
- Configuration Management
- Automated Testing
- Logging
- Data Visualization












    





