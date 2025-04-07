resource "google_pubsub_topic" "veroxe_topic" {
  name = var.pubsub_topic
}

resource "google_pubsub_subscription" "veroxe_sub" {
  name  = var.pubsub_subscription
  topic = google_pubsub_topic.veroxe_topic.id
}