variable "project_id" {
  type        = string
  description = "The GCP project ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
  description = "The GCP region"
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

variable "vertex_featurestore_name" {
  type        = string
  default     = "veroxe-featurestore"
}
variable "vertex_service_account" {
  description = "Service account email used for the Vertex Notebook"
  type        = string
}
