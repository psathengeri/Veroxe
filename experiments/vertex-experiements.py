# experiments/vertex-experiements.py

from google.cloud import aiplatform
import time
import random

# === CONFIGURATION ===
PROJECT_ID = "mlops-veroxe"
LOCATION = "us-central1"
EXPERIMENT_NAME = "veroxe-exp-01"

# === INITIALIZE ===
aiplatform.init(
    project=PROJECT_ID,
    location=LOCATION,
    experiment=EXPERIMENT_NAME  # This will create the experiment if it doesn't exist
)

# Create an experiment run
run_name = f"run-{int(time.time())}"
with aiplatform.start_run(run=run_name) as experiment_run:
    # Log parameters
    experiment_run.log_params({
        "model_type": "logistic_regression",
        "learning_rate": 0.01,
        "batch_size": 32
    })

    # Log metrics
    experiment_run.log_metrics({
        "accuracy": round(random.uniform(0.7, 0.9), 4),
        "loss": round(random.uniform(0.3, 0.5), 4)
    })

# Optionally log an artifact (e.g., local file path or GCS path)
# experiment_run.log_file("model_summary", "/tmp/model.txt")

print(f"Logged experiment run '{run_name}' to experiment '{EXPERIMENT_NAME}'")
