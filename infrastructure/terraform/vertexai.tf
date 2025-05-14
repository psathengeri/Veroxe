# Feature Store configuration - commented out for MVP to reduce costs
# Uncomment when feature store functionality is needed
/*
resource "random_id" "featurestore_name_suffix" {
  byte_length = 4
}

resource "google_vertex_ai_featurestore" "veroxe_featurestore" {
  name     = "veroxe_fs_${random_id.featurestore_name_suffix.hex}"
  region   = var.region
  labels = {
    environment = "testing"
  }

  online_serving_config {
    fixed_node_count = 1
  }

  force_destroy = true
}
*/

resource "random_id" "endpoint_suffix" {
  byte_length = 4
}

resource "google_vertex_ai_endpoint" "model_endpoint" {
  name         = "veroxe-model-endpoint-${random_id.endpoint_suffix.hex}"
  display_name = "Veroxe Model Endpoint"
  location     = var.region

  
  # Remove network configuration for now as it's optional
  # network      = "projects/${var.project_number}/global/networks/default"
}

# Vertex AI Experiment tracking
resource "google_vertex_ai_tensorboard" "experiment" {
  display_name = "experiment-veroxe-01"
  description  = "Tensorboard for tracking ML experiments"
  region      = var.region
}

# Model Registry bucket
resource "google_storage_bucket" "model_registry" {
  name          = "veroxe-model-registry"
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }
}

# Pipeline storage
resource "google_storage_bucket" "pipeline_storage" {
  name          = "pipeline-veroxe-train"
  location      = var.region
  force_destroy = false

  uniform_bucket_level_access = true
}

# Monitoring resources
resource "google_monitoring_dashboard" "ml_monitoring" {
  dashboard_json = jsonencode({
    displayName = "ML Model Monitoring"
    gridLayout = {
      columns = "2"
      widgets = [
        {
          title = "Model Prediction Requests"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"aiplatform.googleapis.com/prediction/online/request_count\""
                }
              }
            }]
          }
        },
        {
          title = "Model Latency"
          xyChart = {
            dataSets = [{
              timeSeriesQuery = {
                timeSeriesFilter = {
                  filter = "metric.type=\"aiplatform.googleapis.com/prediction/online/latencies\""
                }
              }
            }]
          }
        }
      ]
    }
  })
}

# Dataflow job template
resource "google_dataflow_job" "preprocessing_pipeline" {
  name              = "veroxe-preprocessing-pipeline"
  temp_gcs_location = "${google_storage_bucket.pipeline_storage.url}/temp"
  template_gcs_path = "gs://dataflow-templates/latest/Word_Count"
  service_account_email = google_service_account.veroxe_sa.email
  
  parameters = {
    inputFile = "${google_storage_bucket.ml_dataset.url}/uploads/pending/*"
    output    = "${google_storage_bucket.ml_dataset.url}/uploads/processed"
  }

  zone = var.zone
}

