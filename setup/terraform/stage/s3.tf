terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.env_bucket_region
  # Credentials follow the standard AWS provider lookup (env vars, shared config, etc.)
}

resource "random_id" "env_bucket_suffix" {
  count = var.create_env_bucket ? 1 : 0
  byte_length = 4
}

resource "aws_s3_bucket" "env_bucket" {
  count = var.create_env_bucket ? 1 : 0

  bucket = "${var.env_bucket_name_prefix}-${random_id.env_bucket_suffix[0].hex}"
  force_destroy = false

  tags = {
    Name    = "aitutor-env-bucket"
    Project = "aitutor"
  }
}

resource "aws_s3_bucket_public_access_block" "env_bucket_block" {
  count = var.create_env_bucket ? 1 : 0
  bucket = aws_s3_bucket.env_bucket[0].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_acl" "env_bucket_acl" {
  count  = var.create_env_bucket ? 1 : 0
  bucket = aws_s3_bucket.env_bucket[0].id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "env_bucket_versioning" {
  count = var.create_env_bucket ? 1 : 0
  bucket = aws_s3_bucket.env_bucket[0].id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "env_bucket_sse" {
  count  = var.create_env_bucket ? 1 : 0
  bucket = aws_s3_bucket.env_bucket[0].id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "env_bucket_lifecycle" {
  count  = var.create_env_bucket ? 1 : 0
  bucket = aws_s3_bucket.env_bucket[0].id

  rule {
    id     = "retain"
    status = "Enabled"

    expiration {
      days = 3650
    }
  }
}
