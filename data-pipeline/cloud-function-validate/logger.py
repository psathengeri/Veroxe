from google.cloud import bigquery
from datetime import datetime
import os

# Initialize BigQuery client
bq_client = bigquery.Client()

# Set BigQuery dataset and table
BQ_DATASET = os.getenv("BQ_DATASET", "veroxe_dataset")
BQ_TABLE = os.getenv("BQ_TABLE", "validation_errors")

def log_validation_error(client_id: str, filename: str, error_type: str, error_details: str):
    """
    Logs a validation error to BigQuery.

    Args:
        client_id (str): The client identifier.
        filename (str): The name of the file that failed.
        error_type (str): The type of validation error.
        error_details (str): A human-readable description of the error.
    """
    table_id = f"{bq_client.project}.{BQ_DATASET}.{BQ_TABLE}"
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "client_id": client_id,
        "filename": filename,
        "error_type": error_type,
        "error_details": error_details
    }
    
    errors = bq_client.insert_rows_json(table_id, [row])
    if errors:
        print(f"BigQuery insertion errors: {errors}")
    else:
        print(f"Logged validation error for {filename}.")