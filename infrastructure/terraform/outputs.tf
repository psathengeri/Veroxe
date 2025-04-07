output "bigquery_dataset_id" {
  value = google_bigquery_dataset.veroxe_dataset.dataset_id
}

output "pubsub_topic" {
  value = google_pubsub_topic.veroxe_topic.name
}

output "cloud_run_url" {
  value = google_cloud_run_service.veroxe_api.status[0].url
}

output "vertex_featurestore" {
  value = google_vertex_ai_featurestore.veroxe_featurestore.name
}