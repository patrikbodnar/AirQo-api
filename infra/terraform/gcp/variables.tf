variable "project-id" {
  default = "airqo-250220"
  description = "GCP project ID"
}

variable "project-number" {
  default = "702081712633"
  description = "GCP project number"
}

variable "region" {
  default = "europe-west1"
  description = "Default region"
}

variable "zone" {
  default = "europe-west1-b"
  description = "Default zone"
}

variable "location" {
  default = "EU"
  description = "Default location"
}

variable "os" {
  default = {
    "ubuntu-xenial" = "ubuntu-1604-xenial-v20200129"
    "ubuntu-bionic" = "ubuntu-1804-bionic-v20200916"
    "ubuntu-focal" = "ubuntu-2004-focal-v20220712"
  }
  description = "Operating systems to use"
}

variable "disk_size" {
  default = {
    "tiny"   = "10"
    "small"  = "20"
    "medium" = "100"
    "large"  = "200"
  }
  description = "Disk sizes to use"
}