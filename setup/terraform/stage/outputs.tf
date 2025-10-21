output "server_id" {
  value = hcloud_server.vm.id
}

output "server_ipv4" {
  value = hcloud_server.vm.ipv4_address
}

output "floating_ip_id" {
  description = "The Hetzner floating IP resource id (empty if use_floating_ip is false)"
  value       = var.use_floating_ip ? hcloud_floating_ip.fip[0].id : ""
}

output "env_bucket_name" {
  description = "Name of the created AWS S3 bucket for environment variables (empty if not created)"
  value       = var.create_env_bucket ? aws_s3_bucket.env_bucket[0].bucket : ""
}
