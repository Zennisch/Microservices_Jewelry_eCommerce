resource "google_compute_instance" "jec_vm" {
  name         = "jec"
  machine_type = "n2-highcpu-8"
  zone         = "${var.gcp_region}-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-minimal-2504-plucky-amd64-v20250708"
      size  = 30
      type  = "pd-standard"
    }
  }

  network_interface {
    network       = "default"
    access_config {}
  }

  metadata = {
    ssh-keys = "ray:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICunYr8q+3s1AOOB/sWgQkzxavVQEUC05CShhUe7qi+X"
    startup-script = file("startup-script.sh")
  }

  tags = ["jec", "allow-ssh"]
}

resource "google_compute_firewall" "allow_ssh" {
  name    = "allow-ssh-jec"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-ssh"]
}