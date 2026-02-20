import argparse
import logging
import yaml
import numpy as np
import pandas as pd
import os
import time
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Mini MLOps Pipeline")

    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--config", required=True, help="Path to config YAML file")
    parser.add_argument("--output", required=True, help="Path to output metrics JSON")
    parser.add_argument("--log-file", required=True, help="Path to log file")

    return parser.parse_args()


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def write_error_json(output_path, version, message):
    error_output = {
        "version": version,
        "status": "error",
        "error_message": message
    }

    with open(output_path, "w") as f:
        json.dump(error_output, f, indent=4)

    print(json.dumps(error_output, indent=4))


def main():
    start_time = time.time()
    args = parse_args()
    setup_logging(args.log_file)

    logging.info("Job started")

    version = "unknown"

    try:
        # =========================
        # Load Configuration
        # =========================
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # =========================
        # Load Input Data
        # =========================
        if not os.path.exists(args.input):
            raise FileNotFoundError("Input file does not exist.")

        df = pd.read_csv(args.input)
        df.columns = df.columns.str.strip().str.lower()

        if df.empty:
            raise ValueError("Input CSV file is empty.")

        if "close" not in df.columns:
            raise ValueError("Required column 'close' not found in dataset.")

        rows_processed = len(df)
        logging.info(f"Data loaded: {rows_processed} rows")

        # =========================
        # Rolling Mean
        # =========================
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        logging.info(f"Rolling mean calculated with window={window}")

        # =========================
        # Signal Generation
        # =========================
        df["signal"] = np.where(df["close"] > df["rolling_mean"], 1, 0)
        df["signal"] = df["signal"].fillna(0)
        logging.info("Signals generated")

        # =========================
        # Metrics
        # =========================
        signal_rate = df["signal"].mean()
        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        logging.info(f"Metrics: signal_rate={signal_rate}, rows_processed={rows_processed}")
        logging.info(f"Job completed successfully in {latency_ms}ms")

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        print(json.dumps(metrics, indent=4))

        sys.exit(0)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")

        write_error_json(args.output, version, str(e))

        sys.exit(1)


if __name__ == "__main__":
    main()