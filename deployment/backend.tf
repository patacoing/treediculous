terraform {
  backend "azurerm" {
    resource_group_name  = "treediculous-grp"
    storage_account_name = "treediculousstorageacc"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}