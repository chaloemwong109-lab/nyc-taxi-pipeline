import logging
from datetime import datetime
import pandas as pd

from src.config import TAXI_TYPES, YEAR, MONTHS, LOGS_DIR, OUTPUTS_DIR
from src.ingest import fetch_taxi_data
from src.transform import clean_and_harmonize, export_curated_data
from src.quality import validate_curated_data
from src.analyze import run_analytical_summary

LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    logging.info("=== STARTING REPRODUCIBLE NYC TAXI PIPELINE (H1 2024) ===")
    quality_reports = []

    for taxi in TAXI_TYPES:
        for month in MONTHS:
            logging.info(f"--- Processing {taxi.upper()} for {YEAR}-{month:02d} ---")
            
            # 1. Ingestion
            raw_path = fetch_taxi_data(taxi_type=taxi, year=YEAR, month=month)
            
            # 2. Transformation
            curated_df, initial_rows = clean_and_harmonize(raw_path, taxi, YEAR, month)
            
            # 3. Quality Validation Gate
            q_report = validate_curated_data(curated_df, taxi, YEAR, month, initial_rows)
            quality_reports.append(q_report)
            
            # 4. Save Curated Output
            export_curated_data(curated_df, taxi, YEAR, month)

    # 5. สรุปรายงาน Data Quality
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    q_df = pd.DataFrame(quality_reports)
    q_report_path = OUTPUTS_DIR / "quality_report.csv"
    q_df.to_csv(q_report_path, index=False)
    logging.info(f"Quality report exported to {q_report_path}")

    # 6. Analytics
    logging.info("--- Computing Final Usage Analytics ---")
    summary = run_analytical_summary()
    
    print("\n" + "="*50)
    print("FINAL ANALYTICAL RESULT: MOST USED TAXI TYPE (H1 2024)")
    print("="*50)
    print(summary.to_string(index=False))
    print("="*50 + "\n")
    logging.info("=== PIPELINE EXECUTION COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_pipeline()