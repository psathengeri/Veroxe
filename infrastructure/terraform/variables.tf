variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The default GCP region for resource deployment"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "The default GCP zone for resource deployment"
  type        = string
  default     = "us-central1-a"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  type        = string
  default     = "prod"
}

variable "labels" {
  description = "A map of labels to apply to resources"
  type        = map(string)
  default     = {
    environment = "production"
    managed_by  = "terraform"
    project     = "veroxe"
  }
}

variable "bq_dataset_id" {
  type        = string
  default     = "veroxe_dataset"
}

variable "bq_table_id" {
  type        = string
  default     = "data_validation"
}

variable "pubsub_topic" {
  type        = string
  default     = "data-upload-topic"
}

variable "pubsub_subscription" {
  type        = string
  default     = "data-upload-sub"
}

variable "cloud_run_service_name" {
  type        = string
  default     = "veroxe-api"
}

variable "container_image" {
  type        = string
  description = "Docker image URI for Cloud Run"
}

# Feature Store related variables - commented out for MVP
# Uncomment when feature store functionality is needed
/*
variable "vertex_featurestore_name" {
  type        = string
  default     = "veroxe-featurestore"
}
*/

variable "vertex_service_account" {
  description = "Service account email used for the Vertex Notebook"
  type        = string
}

variable "scorer_image_uri" {
  type        = string
  description = "URI for the scorer service container image (e.g., gcr.io/project/image:tag)"
  default     = "gcr.io/cloudrun/hello:latest"  # Default to a test image
}

variable "user_email" {
  description = "The email address of the user who needs access to the storage bucket"
  type        = string
  default     = "pavan.jerry.business@gmail.com"  # Your email address
}
