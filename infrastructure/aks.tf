
// Resources
resource "azurerm_kubernetes_cluster" "this" {
  name                = var.cluster_name
  location            = azurerm_resource_group.this.location
  resource_group_name = azurerm_resource_group.this.name
  dns_prefix          = var.cluster_dns_prefix

  default_node_pool {
    name       = "default"
    node_count = var.cluster_nodes_count
    vm_size    = var.cluster_node_size
  }

  network_profile {
    network_plugin = "azure"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = local.tags
}

resource "azurerm_public_ip" "k8s" {
  name                = var.project_name
  domain_name_label   = var.project_name
  resource_group_name = azurerm_kubernetes_cluster.this.node_resource_group
  location            = azurerm_kubernetes_cluster.this.location
  allocation_method   = "Static"
  sku                 = "Standard"

  tags = local.tags
}

// Outputs
output "host" {
  value     = azurerm_kubernetes_cluster.this.kube_config.0.host
  sensitive = true
}

output "public_ip_address" {
  value = azurerm_public_ip.k8s.ip_address
}

output "domain" {
  value = azurerm_public_ip.k8s.fqdn
}

output "client_certificate" {
  value     = azurerm_kubernetes_cluster.this.kube_config.0.client_certificate
  sensitive = true
}

output "kube_config" {
  value     = azurerm_kubernetes_cluster.this.kube_config_raw
  sensitive = true
}
