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
    "aiplatform.googleapis.com"
  ])
  service = each.key
}

resource "google_service_account" "vertexai_sa" {
  account_id   = "vertexai-sa"
  display_name = "Vertex AI Custom Service Account"
  project      = var.project_id
}

resource "google_project_iam_member" "vertexai_sa_role" {
  project = var.project_id
  role    = "roles/aiplatform.admin"
  member  = "serviceAccount:${google_service_account.vertexai_sa.email}"
}

# Optional: Grant additional permissions if needed
resource "google_project_iam_member" "vertexai_sa_storage" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.vertexai_sa.email}"
}
