resource "google_cloud_run_service" "veroxe_api" {
  name     = var.cloud_run_service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.container_image
      }
      timeout_seconds = 60 # Adjust this value as needed (in seconds)
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.veroxe_api.name
  location = google_cloud_run_service.veroxe_api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}