# src/ingest.py
import requests
import logging
import time
from pathlib import Path
from src.config import BASE_TLC_URL, DATA_RAW_DIR

def fetch_taxi_data(taxi_type: str, year: int, month: int, max_retries: int = 3) -> Path:
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    target_path = DATA_RAW_DIR / filename
    temp_path = DATA_RAW_DIR / f"{filename}.tmp"

    if target_path.exists() and target_path.stat().st_size > 0:
        logging.info(f"[INGEST CACHE HIT] {filename} exists. Skipping download.")
        return target_path

    url = f"{BASE_TLC_URL}/{filename}"
    
    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"[INGEST DOWNLOAD] (Attempt {attempt}/{max_retries}) Downloading {url}...")
            # timeout=(connect_timeout, read_timeout)
            response = requests.get(url, stream=True, timeout=(20, 300))
            response.raise_for_status()

            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=2 * 1024 * 1024):  # 2MB chunks
                    if chunk:
                        f.write(chunk)
            
            # เมื่อโหลดครบสมบูรณ์ ค่อยเปลี่ยนชื่อไฟล์
            if temp_path.exists():
                temp_path.replace(target_path)

            logging.info(f"[INGEST SUCCESS] Saved to {target_path}")
            return target_path

        except (requests.exceptions.RequestException, Exception) as e:
            logging.warning(f"[INGEST RETRY] Attempt {attempt} failed: {e}")
            if temp_path.exists():
                temp_path.unlink()  # ลบไฟล์ชั่วคราวทิ้ง
            
            if attempt == max_retries:
                logging.error(f"[INGEST FAILED] Could not download {filename} after {max_retries} attempts.")
                raise e
            
            time.sleep(5)  # หน่วงเวลา 5 วินาทีก่อนลองใหม่