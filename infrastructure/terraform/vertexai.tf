resource "google_vertex_ai_featurestore" "veroxe_featurestore" {
  name     = var.vertex_featurestore_name
  region   = var.region
}