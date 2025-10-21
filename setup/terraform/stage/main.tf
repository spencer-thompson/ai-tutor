terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.30"
    }
  }
}

provider "hcloud" {
  # Token selection order:
  # 1. var.hcloud_token (passed via -var or TF_VAR_hcloud_token)
  # 2. HCLOUD_TOKEN parsed from ./.env (if file exists and contains HCLOUD_TOKEN=...)
  # 3. empty string (will result in provider error)
  token = local.hcloud_token_clean
}

locals {
  env_file_path = "${path.module}/.env"
  env_contents  = fileexists(local.env_file_path) ? file(local.env_file_path) : ""

  # Capture HCLOUD_TOKEN value from .env; supports HCLOUD_TOKEN=value or HCLOUD_TOKEN="value"
  # Use try() to avoid index errors when regex doesn't match (handles CRLF/format variations)
  hcloud_token_from_env = try(regexall("(?m)^\\s*HCLOUD_TOKEN\\s*=\\s*\"?([^\"\\r\\n]+)\"?\\s*$", local.env_contents)[0][1], "")

  hcloud_token_final = var.hcloud_token != "" ? var.hcloud_token : local.hcloud_token_from_env

  # Remove surrounding double quotes and whitespace characters (CR/LF) which may come from .env
  hcloud_token_clean = length(local.hcloud_token_final) > 0 ? trim(replace(local.hcloud_token_final, "\"", ""), "\n\r\t ") : ""
}



resource "hcloud_server" "vm" {
  name        = var.instance_name
  server_type = var.server_type
  image       = var.image
  location    = var.location
  ssh_keys    = [var.existing_ssh_key_id]
  user_data   = templatefile("${path.module}/cloud-init.yaml.tpl", {public_key = file(var.ssh_public_key_path), bootstrap = chomp(replace(file("${path.module}/../../setup/bootstrap.sh"), "\r", ""))})
  labels = {
    project = "aitutor"
  }
}

resource "hcloud_floating_ip" "fip" {
  count         = var.use_floating_ip ? 1 : 0
  type          = "ipv4"
  home_location = var.location
}

resource "hcloud_floating_ip_assignment" "fip_assign" {
  count           = var.use_floating_ip ? 1 : 0
  server_id       = hcloud_server.vm.id
  floating_ip_id  = hcloud_floating_ip.fip[0].id
}
