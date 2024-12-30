output "fqdn" {
  value       = azurerm_container_group.this.fqdn
  description = "Fqdn of the container group."
}

output "ip" {
  value       = azurerm_container_group.this.ip_address
  description = "Ip address of the container group."
  sensitive   = true
}