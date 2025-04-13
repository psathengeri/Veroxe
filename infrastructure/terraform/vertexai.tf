resource "random_id" "featurestore_name_suffix" {
  byte_length = 4
}

resource "google_vertex_ai_featurestore" "veroxe_featurestore" {
  name     = "veroxe_fs_${random_id.featurestore_name_suffix.hex}"
  region   = var.region
  labels = {
    environment = "testing"
  }

  online_serving_config {
    fixed_node_count = 1
  }

  force_destroy = true
}

