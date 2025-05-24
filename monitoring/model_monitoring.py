from google.cloud import aiplatform
from google.cloud import bigquery
import json
import logging

# Project configuration
PROJECT_ID = "mlops-veroxe"
REGION = "us-central1"
BQ_DATASET = "veroxe_dataset_21d7351d"
MONITORING_TABLE = "prediction_logs"

class ModelMonitor:
    def __init__(self, project_id: str = PROJECT_ID, location: str = REGION):
        self.project_id = project_id
        self.location = location
        self.client = aiplatform.gapic.ModelMonitoringClient()
        
    def setup_monitoring(
        self,
        model_id: str,
        dataset_id: str = BQ_DATASET,
        table_id: str = MONITORING_TABLE,
        monitoring_interval: str = "3600s"
    ):
        """Set up model monitoring for a deployed model."""
        monitoring_config = {
            "monitoring_interval": monitoring_interval,
            "monitoring_alert_config": {
                "email_alert_config": {
                    "user_emails": ["alerts@veroxe.com"]
                }
            },
            "monitoring_metrics": {
                "prediction_metrics": {
                    "skew_detection_config": {
                        "data_source": f"bq://{self.project_id}.{dataset_id}.{table_id}",
                        "skew_thresholds": {
                            "feature_skew": 0.1,
                            "prediction_skew": 0.1
                        }
                    }
                }
            }
        }
        
        # Create monitoring job
        parent = f"projects/{self.project_id}/locations/{self.location}/models/{model_id}"
        monitoring_job = self.client.create_model_monitoring_job(
            parent=parent,
            model_monitoring_job=monitoring_config
        )
        
        return monitoring_job

    def log_prediction(
        self,
        dataset_id: str = BQ_DATASET,
        table_id: str = MONITORING_TABLE,
        prediction_input: dict = None,
        prediction_output: dict = None,
        model_id: str = None,
        client_id: str = None
    ):
        """Log prediction inputs and outputs to BigQuery."""
        if not all([prediction_input, prediction_output, model_id, client_id]):
            raise ValueError("All parameters must be provided")
            
        client = bigquery.Client()
        table_ref = f"{self.project_id}.{dataset_id}.{table_id}"
        
        row = {
            "timestamp": "CURRENT_TIMESTAMP()",
            "model_id": model_id,
            "client_id": client_id,
            "prediction_input": json.dumps(prediction_input),
            "prediction_output": json.dumps(prediction_output)
        }
        
        errors = client.insert_rows_json(table_ref, [row])
        if errors:
            logging.error(f"Errors inserting rows: {errors}")
            raise Exception(f"Failed to log prediction: {errors}")

def create_monitoring_tables(project_id: str = PROJECT_ID, dataset_id: str = BQ_DATASET):
    """Create necessary BigQuery tables for monitoring."""
    client = bigquery.Client()
    
    # Create predictions log table
    predictions_schema = [
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("model_id", "STRING"),
        bigquery.SchemaField("client_id", "STRING"),
        bigquery.SchemaField("prediction_input", "JSON"),
        bigquery.SchemaField("prediction_output", "JSON")
    ]
    
    table_ref = f"{project_id}.{dataset_id}.{MONITORING_TABLE}"
    table = bigquery.Table(table_ref, schema=predictions_schema)
    table = client.create_table(table, exists_ok=True)
    
    return table 