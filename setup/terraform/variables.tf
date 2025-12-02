variable "hcloud_token" {
  description = "Hetzner Cloud API token"
  type        = string
  sensitive   = true
}

variable "s3_access_key" {
  description = "S3 access key for Hetzner Object Storage"
  type        = string
  sensitive   = true
}

variable "s3_secret_key" {
  description = "S3 secret key for Hetzner Object Storage"
  type        = string
  sensitive   = true
}

variable "ssh_public_key_path" {
  description = "Path to the SSH public key to be used for the VM"
  type        = string
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "ai-tutor-staging"
}

variable "app_port" {
  description = "Port the application will run on"
  type        = number
  default     = 8080
}

variable "ssh_key_name" {
  description = "Name of the existing SSH key in Hetzner Cloud"
  type        = string
  default     = "Landon"
}