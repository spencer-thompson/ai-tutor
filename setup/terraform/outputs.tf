output "vm_ip" {
  description = "The IP address of the staging server"
  value       = hcloud_server.staging_server.ipv4_address
}

output "floating_ip" {
  description = "The floating IP address of the staging server"
  value       = hcloud_floating_ip.staging_ip.ip_address
}
