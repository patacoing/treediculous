provider "azurerm" {
  features {
    machine_learning {
      purge_soft_deleted_workspace_on_destroy = true
    }
  }
}

provider "ovh" {
  endpoint           = local.ovh_endpoint
  application_key    = var.ovh_application_key
  application_secret = var.ovh_application_secret
  consumer_key       = var.ovh_consumer_key
}

locals {
  base_name                 = "treediculous"
  registry_base_name        = "ghcr.io/patacoing/${local.base_name}"
  application_insights_name = "${local.base_name}insights"
  key_vault_name            = "${local.base_name}keyvault"
  storage_account_name      = "${local.base_name}storageacc"
  web_container = {
    name       = "${local.base_name}-web"
    cpu        = 0.5
    memory     = 1
    image_name = "${local.registry_base_name}:${var.web_version}"
  }
  api_container = {
    name       = "${local.base_name}-api"
    cpu        = 1
    memory     = 2
    image_name = "${local.registry_base_name}:${var.api_version}"
  }
  ovh_endpoint = "ovh-eu"
}

resource "azurerm_resource_group" "this" {
  name     = var.resource_group_name
  location = var.location
}

resource "azurerm_application_insights" "this" {
  name                = local.application_insights_name
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  application_type    = "web"
}

data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "this" {
  name                = local.key_vault_name
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"
}

resource "azurerm_storage_account" "this" {
  name                     = local.storage_account_name
  location                 = var.location
  resource_group_name      = azurerm_resource_group.this.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_machine_learning_workspace" "this" {
  name                    = var.workspace_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  application_insights_id = azurerm_application_insights.this.id
  key_vault_id            = azurerm_key_vault.this.id
  storage_account_id      = azurerm_storage_account.this.id

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_container_group" "this" {
  name                = local.base_name
  location            = var.location
  resource_group_name = azurerm_resource_group.this.name
  ip_address_type     = "Public"
  dns_name_label      = local.base_name
  os_type             = "Linux"

  container {
    name   = local.web_container["name"]
    image  = local.web_container["image_name"]
    cpu    = local.web_container["cpu"]
    memory = local.web_container["memory"]

    ports {
      port = 80
    }

    ports {
      port = 443
    }
  }

  container {
    name   = local.api_container["name"]
    image  = local.api_container["image_name"]
    cpu    = local.api_container["cpu"]
    memory = local.api_container["memory"]

    ports {
      port = 8000
    }
  }

  exposed_port {
    port = 80
  }

  exposed_port {
    port = 443
  }
}

resource "ovh_domain_zone_record" "frontend" {
  zone      = var.domain_name
  subdomain = ""
  fieldtype = "A"
  ttl       = 3600
  target    = azurerm_container_group.this.ip_address
}

resource "ovh_domain_zone_record" "backend" {
  zone      = var.domain_name
  subdomain = "backend"
  fieldtype = "A"
  ttl       = 3600
  target    = azurerm_container_group.this.ip_address
}