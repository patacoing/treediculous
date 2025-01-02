terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.14.0"
    }

    ovh = {
      source  = "ovh/ovh"
      version = "1.4.0"
    }
  }
  required_version =  "1.5.7"
}