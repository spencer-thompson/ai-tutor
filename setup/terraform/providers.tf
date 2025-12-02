terraform {
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.0"
    }
    s3 = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

provider "aws" {
  access_key = var.s3_access_key
  secret_key = var.s3_secret_key
  region     = "us-east-1" # This is a placeholder, but required by the provider

  endpoints {
    s3 = "https://hel1.your-objectstorage.com"
  }
}
