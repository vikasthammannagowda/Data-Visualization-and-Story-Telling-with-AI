#!/usr/bin/env python3
import time
import datetime
import csv
import json
from pathlib import Path
import logging
import Adafruit_DHT

# Optional sensor imports; fail gracefully if missing
try:
    import board
    import busio
    import adafruit_tsl2561
    from adafruit_ads1x15.ads1115 import ADS1115
    from adafruit_ads1x15.analog_in import AnalogIn
except ImportError:
    board = None
    busio = None
    adafruit_tsl2561 = None
    ADS1115 = None
    AnalogIn = None

# ---------- CONFIGURATION ----------
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin (BCM) connected to DHT22 data line
SAMPLE_INTERVAL_SEC = 120  # every 2 minutes; adjust 60-300 as needed
RUN_DURATION_DAYS = 5
MAX_RETRIES = 3
RETRY_DELAY_SEC = 5
LOCATION_LABEL = "room_corner"  # change per deployment
BIAS_INTRODUCED = False
BIAS_DESCRIPTION = ""  # e.g., "Placed near direct sunlight for radiative heating bias"

# Output files
out_dir = Path("env_run_output")
out_dir.mkdir(exist_ok=True)
start_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
data_path = out_dir / f"environment_log_{LOCATION_LABEL}_{start_ts}.tsv"
meta_path = out_dir / f"deployment_meta_{LOCATION_LABEL}_{start_ts}.json"
log_path = out_dir / f"collector_health_{LOCATION_LABEL}_{start_ts}.log"

# ---------- LOGGING ----------
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("env_collector")

# ---------- SENSOR INITIALIZATION ----------
ads = None
light_sensor = None
if ADS1115 and AnalogIn and busio and board:
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = ADS1115(i2c)
        # Optionally set gain here if needed, e.g., ads.gain = 1
    except Exception as e:
        logger.warning(f"Failed to init ADS1115 ADC: {e}")
    if adafruit_tsl2561:
        try:
            light_sensor = adafruit_tsl2561.TSL2561(i2c)
            light_sensor.enable = True
            # optional: light_sensor.integration_time = 0x02
        except Exception as e:
            logger.warning(f"Failed to init TSL2561: {e}")
else:
    logger.warning("Analog/light sensor libraries missing or I2C unavailable; some reads will be None.")

# ---------- METADATA ----------
metadata = {
    "start_time_iso": None,
    "location_label": LOCATION_LABEL,
    "sensors": {
        "temperature_humidity": "DHT22",
        "air_quality_proxy": "Analog via ADS1115 (e.g., MQ135)",
        "light": "TSL2561 or LDR"
    },
    "sample_interval_sec": SAMPLE_INTERVAL_SEC,
    "run_duration_days": RUN_DURATION_DAYS,
    "bias_introduced": BIAS_INTRODUCED,
    "bias_description": BIAS_DESCRIPTION,
    "calibration": {
        "mq135_baseline_raw": None,
        "dht_offset_temp_C": 0.0,
        "dht_offset_humidity_pct": 0.0
    },
    "notes": ""
}

# ---------- FILE INITIALIZATION ----------
if not data_path.exists():
    with open(data_path, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow([
            "timestamp_iso",
            "unix_time",
            "temperature_C",
            "humidity_percent",
            "air_quality_raw",
            "light_lux",
            "read_attempts",
            "sensor_status",  # OK / PARTIAL_FAIL / FAIL
            "notes"
        ])

# ---------- HELPER READS ----------
def read_dht():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def read_mq135_raw():
    if ads:
        try:
            # Depending on library version: AnalogIn(ads, ADS1115.P0) or channel index
            chan = AnalogIn(ads, 0)  # using channel 0; adjust if wiring differs
            return chan.value  # raw integer
        except Exception as e:
            logger.warning(f"MQ135 raw read error: {e}")
            return None
    return None

def read_light():
    if light_sensor:
        try:
            # returns lux; may be None if in very low light
            return light_sensor.lux
        except Exception as e:
            logger.warning(f"Light sensor read error: {e}")
            return None
    # Placeholder for LDR if wired through ADC: implement similar to read_mq135_raw
    return None

def perform_sample():
    attempts = 0
    temp = hum = air_raw = light = None
    notes = []
    sensor_status = "OK"
    while attempts < MAX_RETRIES:
        # DHT read
        try:
            temp, hum = read_dht()
            if temp is None or hum is None:
                raise ValueError("DHT returned None")
        except Exception as e:
            notes.append(f"DHT error: {e}")
        # MQ135
        try:
            air_raw = read_mq135_raw()
            if air_raw is None:
                raise ValueError("Air quality read None")
        except Exception as e:
            notes.append(f"Air quality error: {e}")
        # Light
        try:
            light = read_light()
        except Exception as e:
            notes.append(f"Light read error: {e}")

        # Determine status
        if all(v is not None for v in [temp, hum, air_raw, light]):
            sensor_status = "OK"
            break
        elif any(v is not None for v in [temp, hum, air_raw, light]):
            sensor_status = "PARTIAL_FAIL"
        else:
            sensor_status = "FAIL"

        attempts += 1
        time.sleep(RETRY_DELAY_SEC)

    return {
        "temperature_C": temp,
        "humidity_percent": hum,
        "air_quality_raw": air_raw,
        "light_lux": light,
        "read_attempts": attempts + 1,
        "sensor_status": sensor_status,
        "notes": "; ".join(notes) if notes else ""
    }

# ---------- INITIAL CALIBRATION ----------
def calibrate_mq135_baseline(samples=5, delay=2):
    vals = []
    for i in range(samples):
        raw = read_mq135_raw()
        if raw is not None:
            vals.append(raw)
        time.sleep(delay)
    if vals:
        baseline = sum(vals) / len(vals)
        metadata["calibration"]["mq135_baseline_raw"] = baseline
        logger.info(f"Captured MQ135 baseline (raw average) = {baseline}")
    else:
        metadata["notes"] += "Failed to capture MQ135 baseline. "

# ---------- MAIN LOOP ----------
def main():
    metadata["start_time_iso"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    # initial calibration for MQ135 baseline (assumes relatively clean air)
    calibrate_mq135_baseline()
    # dump initial metadata
    with open(meta_path, "w") as mf:
        json.dump(metadata, mf, indent=2)

    end_time = time.time() + RUN_DURATION_DAYS * 86400
    logger.info(f"Starting data collection until {datetime.datetime.fromtimestamp(end_time)}")

    while time.time() < end_time:
        loop_start = time.time()
        sample = perform_sample()
        ts = datetime.datetime.now(datetime.timezone.utc)
        row = [
            ts.isoformat(),
            int(ts.timestamp()),
            sample["temperature_C"],
            sample["humidity_percent"],
            sample["air_quality_raw"],
            sample["light_lux"],
            sample["read_attempts"],
            sample["sensor_status"],
            sample["notes"]
        ]
        with open(data_path, "a", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(row)

        # update metadata heartbeat
        metadata["last_sample_iso"] = ts.isoformat()
        with open(meta_path, "w") as mf:
            json.dump(metadata, mf, indent=2)

        # wait until next interval accounting for execution time
        elapsed = time.time() - loop_start
        to_sleep = SAMPLE_INTERVAL_SEC - elapsed
        if to_sleep > 0:
            time.sleep(to_sleep)

    logger.info("Completed data collection.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Interrupted by user; exiting.")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
