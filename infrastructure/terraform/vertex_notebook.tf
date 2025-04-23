resource "google_notebooks_instance" "veroxe_notebook" {
  name         = "veroxe-notebook"
  location     = var.region
  project      = var.project_id
  machine_type = "n1-standard-2"

  vm_image {
    project = "deeplearning-platform-release"
    family  = "common-cpu-notebooks"
  }

  service_account = var.vertex_service_account

  metadata = {
    proxy-mode = "project_editors"
  }
}
