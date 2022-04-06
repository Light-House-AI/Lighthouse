project_name        = "lighthouse-ai"
resource_group_name = "rg-lighthouse"
environment         = "production"
location            = "westeurope"

cluster_name        = "lighthouse-ai"
cluster_dns_prefix  = "lighthouse-ai"
cluster_nodes_count = 2
cluster_node_size   = "Standard_B2s"

storage_account_name = "lighthouseai"

postgres_server_name           = "lighthouse-ai-postgres"
postgres_server_admin_user     = "admin"
postgres_server_admin_password = "admin"
postgres_server_db_name        = "admin"
