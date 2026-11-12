import pandas as pd
import logging

def validate_curated_data(df: pd.DataFrame, taxi_type: str, year: int, month: int, initial_rows: int) -> dict:
    cleaned_rows = len(df)
    dropped_rows = initial_rows - cleaned_rows
    
    negative_distance = int((df["trip_distance"] < 0).sum()) if "trip_distance" in df.columns else 0
    
    start_date = f"{year}-{month:02d}-01"
    next_m = month + 1 if month < 12 else 1
    next_y = year if month < 12 else year + 1
    end_date = f"{next_y}-{next_m:02d}-01"
    
    out_of_range = int((~((df["pickup_datetime"] >= start_date) & (df["pickup_datetime"] < end_date))).sum())

    passed = (negative_distance == 0) and (out_of_range == 0)

    report = {
        "taxi_type": taxi_type,
        "month": month,
        "raw_records": initial_rows,
        "curated_records": cleaned_rows,
        "dropped_records": dropped_rows,
        "negative_distance_left": negative_distance,
        "out_of_range_dates_left": out_of_range,
        "quality_gate_passed": passed
    }
    
    status = "PASSED" if passed else "FAILED"
    logging.info(f"[QUALITY GATE - {status}] {taxi_type} (M{month:02d}): Validated {cleaned_rows:,} records.")
    return report