resource "google_cloud_run_service" "veroxe_scorer" {
  name     = "veroxe-scorer-service"
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.veroxe_sa.email
      containers {
        image = var.scorer_image_uri
        
        resources {
          limits = {
            cpu    = "2.0"
            memory = "4Gi"
          }
        }

        env {
          name  = "PROJECT_ID"
          value = var.project_id
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  lifecycle {
    ignore_changes = [
      template[0].spec[0].containers[0].image,
    ]
  }
}

# Allow unauthenticated access to the service
resource "google_cloud_run_service_iam_member" "scorer_public_access" {
  service  = google_cloud_run_service.veroxe_scorer.name
  location = google_cloud_run_service.veroxe_scorer.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Cloud Function for data preprocessing
resource "google_storage_bucket" "function_source" {
  name                        = "veroxe-functions-source"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = true
  
  public_access_prevention    = "enforced"
}

# Grant permissions to the service account
resource "google_storage_bucket_iam_binding" "function_source_access" {
  bucket = google_storage_bucket.function_source.name
  role   = "roles/storage.objectViewer"
  members = [
    "serviceAccount:${google_service_account.veroxe_sa.email}",
    "user:${var.user_email}"  # Add your email here
  ]
}

# Grant additional permissions for object creation and management
resource "google_storage_bucket_iam_binding" "function_source_admin" {
  bucket = google_storage_bucket.function_source.name
  role   = "roles/storage.objectAdmin"
  members = [
    "serviceAccount:${google_service_account.veroxe_sa.email}",
    "user:${var.user_email}"  # Add your email here
  ]
}

resource "random_id" "function_name_suffix" {
  byte_length = 4
}

# Create a local file for the function source
resource "local_file" "function_source" {
  filename = "${path.module}/function_source/main.py"
  content  = <<-EOF
def process_data(request):
    return 'Hello World!'
EOF
}

# Create requirements.txt
resource "local_file" "requirements" {
  filename = "${path.module}/function_source/requirements.txt"
  content  = ""  # Empty requirements for now
}

# Create the source archive
data "archive_file" "function_source" {
  type        = "zip"
  output_path = "${path.module}/function_source.zip"
  source_dir  = "${path.module}/function_source"
  depends_on  = [local_file.function_source, local_file.requirements]
}

# Upload the source code archive to GCS
resource "google_storage_bucket_object" "function_source" {
  name   = "function-source-${data.archive_file.function_source.output_md5}.zip"
  bucket = google_storage_bucket.function_source.name
  source = data.archive_file.function_source.output_path

  depends_on = [
    google_storage_bucket_iam_binding.function_source_access,
    google_storage_bucket_iam_binding.function_source_admin
  ]
}

resource "google_cloudfunctions_function" "data_preprocessor" {
  name        = "veroxe-data-preprocessor-${random_id.function_name_suffix.hex}"
  description = "Function for preprocessing incoming data"
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_source.name
  source_archive_object = google_storage_bucket_object.function_source.name
  trigger_http         = true
  entry_point         = "process_data"

  service_account_email = google_service_account.veroxe_sa.email

  environment_variables = {
    PROJECT_ID = var.project_id
    DATASET_ID = google_bigquery_dataset.veroxe_dataset.dataset_id
  }
} 