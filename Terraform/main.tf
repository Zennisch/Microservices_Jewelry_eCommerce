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
    ssh-keys = var.ssh_public_key
    startup-script = file("startup-script.sh")
  }

  tags = ["jec", "allow-ssh", "allow-app-ports"]
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

resource "google_compute_firewall" "allow_app_ports_3000" {
  name    = "allow-app-ports-3000-jec"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["3000-3009"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-app-ports"]
}

resource "google_compute_firewall" "allow_app_port_5000" {
  name    = "allow-app-port-5000-jec"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-app-ports"]
}

resource "google_compute_firewall" "allow_app_ports_8000" {
  name    = "allow-app-ports-8000-jec"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["8000-8009"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["allow-app-ports"]
}