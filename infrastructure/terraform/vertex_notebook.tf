resource "google_workbench_instance" "veroxe_notebook" {
  name     = "veroxe-notebook"
  location = var.zone
  project  = var.project_id

  gce_setup {
    machine_type = "e2-standard-4"
    
    container_image {
      repository = "gcr.io/deeplearning-platform-release/base-cpu"
      tag        = "latest"
    }

    boot_disk {
      disk_type    = "PD_SSD"
      disk_size_gb = 150
    }

    network_interfaces {
      network = "projects/${var.project_id}/global/networks/default"
    }

    service_accounts {
      email = var.vertex_service_account
    }

    disable_public_ip = false

    metadata = {
      proxy-mode = "service_account"
      terraform  = "true"
    }

    tags = ["vertex-workbench"]
  }

  labels = {
    environment = "dev"
    purpose     = "ml-development"
    managed_by  = "terraform"
  }

  timeouts {
    create = "45m"
    delete = "30m"
  }

  depends_on = [
    google_project_service.required
  ]
}
