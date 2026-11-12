import pandas as pd
import logging
from src.config import DATA_CURATED_DIR, OUTPUTS_DIR

def run_analytical_summary() -> pd.DataFrame:
    curated_files = sorted(list(DATA_CURATED_DIR.glob("curated_*.parquet")))
    if not curated_files:
        raise FileNotFoundError("Curated parquet files not found in data/curated/")

    records = []
    for f in curated_files:
        temp_df = pd.read_parquet(f, columns=["taxi_type"])
        count = len(temp_df)
        t_type = temp_df["taxi_type"].iloc[0]
        records.append({"file": f.name, "taxi_type": t_type, "trip_count": count})

    df_records = pd.DataFrame(records)
    summary = df_records.groupby("taxi_type", as_index=False)["trip_count"].sum()

    total_trips = summary["trip_count"].sum()
    summary["market_share_pct"] = ((summary["trip_count"] / total_trips) * 100).round(2)
    summary = summary.sort_values(by="trip_count", ascending=False).reset_index(drop=True)

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = OUTPUTS_DIR / "summary_metrics.csv"
    summary.to_csv(summary_path, index=False)

    logging.info(f"[ANALYTICS] Summary results saved to {summary_path}")
    return summary