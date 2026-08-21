terraform {
  required_version = ">= 1.15.9"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.61.0"
    }
  }
  backend "s3" {
    bucket  = "mvtthxw-tf-state"
    key     = "state/python-monolit-ecr.tfstate"
    region  = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = {
      Owner       = var.username
      Repo        = var.repo
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
