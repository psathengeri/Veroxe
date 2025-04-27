resource "google_pubsub_topic" "data_upload" {
  name = "data-upload-topic"
}

resource "google_pubsub_subscription" "data_upload" {
  name  = "data-upload-sub"
  topic = google_pubsub_topic.data_upload.name

  ack_deadline_seconds = 20

  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering = true
}