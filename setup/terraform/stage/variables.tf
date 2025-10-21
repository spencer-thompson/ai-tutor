variable "hcloud_token" {
  description = "Hetzner Cloud API token. It's recommended to set via environment variable HCLOUD_TOKEN and tf var via -var 'hcloud_token=$HCLOUD_TOKEN'"
  type        = string
  default     = ""
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key to upload"
  type        = string
  default     = "~/.ssh/id_ed25519.pub"
}

variable "ssh_key_name" {
  description = "Name to give the uploaded SSH key in Hetzner"
  type        = string
  default     = ""
}

variable "instance_name" {
  description = "Name for the server resource"
  type        = string
  default     = "aitutor-cx23"
}

variable "image" {
  description = "Server image to use"
  type        = string
  default     = "ubuntu-22.04"
}

variable "server_type" {
  description = "Hetzner server type"
  type        = string
  default     = "cx23"
}

variable "location" {
  description = "Hetzner location/zone"
  type        = string
  default     = "hel1"
}

variable "use_floating_ip" {
  description = "Whether to allocate and assign a floating IPv4 address"
  type        = bool
  default     = true
}

variable "existing_ssh_key_id" {
  description = "ID of an existing Hetzner SSH key to use for server access"
  type        = string
  default     = ""
}

variable "create_env_bucket" {
  description = "Whether to create an AWS S3 bucket to store environment variables (optional)."
  type        = bool
  default     = false
}

variable "env_bucket_name_prefix" {
  description = "Prefix to use when creating the S3 bucket. A random suffix will be appended to ensure uniqueness."
  type        = string
  default     = "aitutor-env"
}

variable "env_bucket_region" {
  description = "AWS region to create the S3 bucket in when create_env_bucket is true."
  type        = string
  default     = "us-east-1"
}
