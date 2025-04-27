resource "google_storage_bucket" "ml_dataset" {
  name          = "ml-dataset-veroxe"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true
  
  lifecycle_rule {
    condition {
      age = 90
    }
    action {
      type = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}

# Create the bucket folder structure
resource "google_storage_bucket_object" "folders" {
  for_each = toset([
    "archived/",
    "downloads/",
    "downloads/private/",
    "downloads/public/",
    "schemas/",
    "uploads/",
    "uploads/failed/",
    "uploads/pending/",
    "uploads/processed/"
  ])

  bucket = google_storage_bucket.ml_dataset.name
  name   = each.key
  content = " "  # Empty content for folder creation
} 