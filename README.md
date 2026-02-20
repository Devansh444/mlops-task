# MLOps Engineering Internship - Technical Assessment

## Overview

This project implements a miniature MLOps-style batch pipeline.

It demonstrates:

- Reproducibility using a configuration file
- Structured logging
- Machine-readable metrics output
- Proper error handling
- Docker-based deployment
- Deterministic execution

The application processes cryptocurrency OHLCV data and generates a trading signal metric based on a rolling mean of the close price.

---

## How the Pipeline Works

1. Load configuration from config.yaml.
2. Set a fixed random seed for reproducibility.
3. Load data.csv.
4. Compute rolling mean on the close column.
5. Generate signals:
   - 1 if close > rolling_mean
   - 0 otherwise
6. Calculate signal rate.
7. Write results to metrics.json.
8. Log execution details in run.log.

---

## Project Structure

mlops-task/
│
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json
└── run.log

---

## Configuration File (config.yaml)

seed: 42
window: 5
version: "v1"

- seed ensures reproducible results
- window defines rolling mean window
- version is included in output metrics

---

## Local Execution

Step 1: Install dependencies

pip install -r requirements.txt

Step 2: Run the application

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

After execution:
- metrics.json is generated
- run.log contains structured logs
- Metrics are printed to stdout

---

## Docker Execution (Mandatory)

Step 1: Build image

docker build -t mlops-task .

Step 2: Run container

docker run --rm mlops-task

The container:
- Executes automatically
- Prints metrics to stdout
- Exits with code 0 on success
- Exits with non-zero code on failure

---

## Example Output (metrics.json)

Success:

{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}

Error:

{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}

---

## Dependencies

- pandas
- numpy
- pyyaml

---

## Key MLOps Concepts Demonstrated

- Configuration-driven pipeline
- Deterministic execution
- Structured logging
- Machine-readable metrics
- Dockerized batch processing
- Robust error handling

---

## Final Note

This project simulates a simplified production-style trading signal pipeline aligned with real-world MLOps practices.