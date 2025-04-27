resource "random_id" "bq_dataset_suffix" {
  byte_length = 4
}

resource "google_bigquery_dataset" "veroxe_dataset" {
  dataset_id                 = "veroxe_dataset_${random_id.bq_dataset_suffix.hex}"
  friendly_name             = "Veroxe ML Dataset"
  description               = "Dataset for Veroxe ML operations"
  location                  = var.region
  delete_contents_on_destroy = false

  labels = {
    environment = "production"
  }

  access {
    role          = "OWNER"
    user_by_email = google_service_account.veroxe_sa.email
  }

  access {
    role          = "READER"
    special_group = "projectReaders"
  }
}

# Commented out until we have the proper schema file
# resource "google_bigquery_table" "veroxe_table" {
#   dataset_id = google_bigquery_dataset.veroxe_dataset.dataset_id
#   table_id   = var.bq_table_id
#   schema     = file("${path.module}/schemas/bq_schema.json")
# }