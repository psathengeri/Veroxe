resource "google_bigquery_dataset" "veroxe_dataset" {
  dataset_id                  = var.bq_dataset_id
  location                    = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_table" "veroxe_table" {
  dataset_id = google_bigquery_dataset.veroxe_dataset.dataset_id
  table_id   = var.bq_table_id
  schema     = file("${path.module}/schemas/bq_schema.json")  # Comment this out for now
}