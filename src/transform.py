import pandas as pd
import logging
from pathlib import Path
from src.config import COLUMN_MAPPINGS, FINAL_SCHEMA_COLS, DATA_CURATED_DIR

def clean_and_harmonize(raw_path: Path, taxi_type: str, year: int, month: int) -> tuple[pd.DataFrame, int]:
    mapping = COLUMN_MAPPINGS[taxi_type]
    raw_cols = list(mapping.keys())
    
    df = pd.read_parquet(raw_path, columns=raw_cols)
    initial_count = len(df)

    df = df.rename(columns=mapping)
    df["taxi_type"] = taxi_type

    df["pickup_datetime"] = pd.to_datetime(df["pickup_datetime"])
    df["dropoff_datetime"] = pd.to_datetime(df["dropoff_datetime"])

    start_date = f"{year}-{month:02d}-01"
    next_m = month + 1 if month < 12 else 1
    next_y = year if month < 12 else year + 1
    end_date = f"{next_y}-{next_m:02d}-01"
    
    df = df[(df["pickup_datetime"] >= start_date) & (df["pickup_datetime"] < end_date)]

    if "trip_distance" in df.columns:
        df = df[(df["trip_distance"].isna()) | (df["trip_distance"] >= 0)]

    curated_df = df[FINAL_SCHEMA_COLS].copy()
    return curated_df, initial_count

def export_curated_data(df: pd.DataFrame, taxi_type: str, year: int, month: int) -> Path:
    DATA_CURATED_DIR.mkdir(parents=True, exist_ok=True)
    curated_file = DATA_CURATED_DIR / f"curated_{taxi_type}_{year}_{month:02d}.parquet"
    df.to_parquet(curated_file, index=False, engine="pyarrow", compression="snappy")
    
    sample_file = DATA_CURATED_DIR / f"sample_{taxi_type}_{year}_{month:02d}.parquet"
    if not sample_file.exists():
        df.head(1000).to_parquet(sample_file, index=False, engine="pyarrow")
        
    logging.info(f"[CURATED EXPORT] Saved to {curated_file}")
    return curated_file