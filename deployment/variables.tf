variable "resource_group_name" {
  description = "The name of the resource group in which to create the resources."
  type        = string
  default     = "treediculous-grp"
}

variable "workspace_name" {
  description = "The name of the azureml workspace."
  type        = string
  default     = "treediculous-ml-grp"
}

variable "location" {
  description = "The location where to deploy resources."
  type        = string
  default     = "northeurope"
}

variable "subscription_id" {
  description = "The subscription id to use."
  type        = string
  sensitive   = true
}

variable "api_version" {
  description = "The api tag to deploy."
  type        = string
  validation {
    condition     = can(regex("api-\\d\\.\\d\\.\\d", var.api_version))
    error_message = "The api version must match the tags' format."
  }
}

variable "web_version" {
  description = "The web tag to deploy."
  type        = string
  validation {
    condition     = can(regex("web-\\d\\.\\d\\.\\d", var.web_version))
    error_message = "The web version must match the tags' format."
  }
}

variable "domain_name" {
  description = "Domain name to use"
  type        = string
  default     = "treediculous.fr"
}

variable "ovh_application_key" {
  description = "Ovh application key to use."
  type        = string
  sensitive   = true
}

variable "ovh_application_secret" {
  description = "Ovh application secret to use."
  type        = string
  sensitive   = true
}

variable "ovh_consumer_key" {
  description = "Ovh consumer key to use."
  type        = string
  sensitive   = true
}