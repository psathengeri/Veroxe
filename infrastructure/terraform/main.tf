provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.3.0"
}

resource "google_project_service" "required" {
  for_each = toset([
    "compute.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "bigquery.googleapis.com",
    "pubsub.googleapis.com",
    "run.googleapis.com",
    "aiplatform.googleapis.com",
    "dataflow.googleapis.com",
    "cloudfunctions.googleapis.com",
    "monitoring.googleapis.com",
    "dataprep.googleapis.com",
    "notebooks.googleapis.com",
    "artifactregistry.googleapis.com",
    "servicenetworking.googleapis.com"
  ])
  service = each.key
  disable_on_destroy = false
}

resource "google_service_account" "veroxe_sa" {
  account_id   = "veroxe-service-account"
  display_name = "Veroxe ML Service Account"
  project      = var.project_id
}

# Grant necessary IAM roles
resource "google_project_iam_member" "veroxe_sa_roles" {
  for_each = toset([
    "roles/aiplatform.user",
    "roles/storage.admin",
    "roles/bigquery.admin",
    "roles/dataflow.developer",
    "roles/pubsub.publisher",
    "roles/pubsub.subscriber",
    "roles/run.invoker"
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.veroxe_sa.email}"
}
