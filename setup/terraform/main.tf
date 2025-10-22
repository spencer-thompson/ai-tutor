data "hcloud_ssh_key" "deploy_key" {
  name = var.ssh_key_name
}

resource "hcloud_server" "staging_server" {
  name        = "ai-tutor-staging-server"
  server_type = "cx23"
  image       = "ubuntu-22.04"
  ssh_keys    = [data.hcloud_ssh_key.deploy_key.id]
  user_data   = templatefile("${path.module}/user_data.tpl", {
    s3_access_key = var.s3_access_key
    s3_secret_key = var.s3_secret_key
    bucket_name   = var.bucket_name
    app_port      = var.app_port
  })
}

resource "hcloud_floating_ip" "staging_ip" {
  type             = "ipv4"
  server_id        = hcloud_server.staging_server.id
  home_location    = "fsn1"
}

resource "hcloud_firewall" "staging_firewall" {
  name = "ai-tutor-staging-firewall"

  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "22"
    source_ips = [
      "0.0.0.0/0",
      "::/0",
    ]
  }

  rule {
    direction = "in"
    protocol  = "tcp"
    port      = var.app_port
    source_ips = [
      "0.0.0.0/0",
      "::/0",
    ]
  }
}
