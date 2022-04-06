
variable "project_name" {
  description = "The name of your project."
  type        = string
}

variable "resource_group_name" {
  description = "The name of your Azure Resource Group."
  type        = string
}

variable "location" {
  description = "The Azure region where your cluster will be created."
  type        = string
}

variable "cluster_name" {
  description = "The name of your Azure Kubernetes Cluster."
  default     = "lighthouse"
}

variable "cluster_dns_prefix" {
  description = "The dns prefix of your Azure Kubernetes Cluster."
  default     = "lighthouse"
}

variable "cluster_nodes_count" {
  description = "The number of nodes which should exist in the node pool."
  default     = 2
}

variable "cluster_node_size" {
  description = "The The size of the virtual machine."
  default     = "Standard_B2s"
}

variable "storage_account_name" {
  description = "The name of your Azure Storage Account."
  type        = string
}

variable "environment" {
  description = "The environment to deploy to."
  default     = "production"
}

variable "postgres_server_name" {
  description = "The name of your PostgreSQL server."
  type        = string
}

variable "postgres_server_admin_user" {
  description = "The admin user for your PostgreSQL server."
  type        = string
}

variable "postgres_server_admin_password" {
  description = "The admin password for your PostgreSQL server."
  type        = string
}

variable "postgres_server_db_name" {
  description = "The name of your PostgreSQL database."
  type        = string
}

locals {
  tags = {
    "project"     = var.project_name,
    "environment" = var.environment
  }
}
