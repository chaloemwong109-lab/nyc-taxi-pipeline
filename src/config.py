from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_CURATED_DIR = BASE_DIR / "data" / "curated"
LOGS_DIR = BASE_DIR / "logs"
OUTPUTS_DIR = BASE_DIR / "outputs"

YEAR = 2024
MONTHS = [1, 2, 3, 4, 5, 6]
TAXI_TYPES = ["yellow", "green", "fhvhv"]

BASE_TLC_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

COLUMN_MAPPINGS = {
    "yellow": {
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
        "PULocationID": "pulocation_id",
        "DOLocationID": "dolocation_id",
        "trip_distance": "trip_distance",
    },
    "green": {
        "lpep_pickup_datetime": "pickup_datetime",
        "lpep_dropoff_datetime": "dropoff_datetime",
        "PULocationID": "pulocation_id",
        "DOLocationID": "dolocation_id",
        "trip_distance": "trip_distance",
    },
    "fhvhv": {
        "pickup_datetime": "pickup_datetime",
        "dropoff_datetime": "dropoff_datetime",
        "PULocationID": "pulocation_id",
        "DOLocationID": "dolocation_id",
        "trip_miles": "trip_distance",
    }
}

FINAL_SCHEMA_COLS = [
    "taxi_type",
    "pickup_datetime",
    "dropoff_datetime",
    "pulocation_id",
    "dolocation_id",
    "trip_distance"
]