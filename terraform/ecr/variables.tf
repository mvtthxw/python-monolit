# General
variable "username" {
  type        = string
  description = "The username of the person deploying the infrastructure"
}

variable "repo" {
  type        = string
  description = "The repository name where the Terraform code is stored"
}

variable "region" {
  type        = string
  description = "The AWS region to deploy resources in"
}

variable "environment" {
  type        = string
  description = "The environment for the deployment (e.g., dev, prod)"
}

# ECR
variable "repository_name" {
  type        = string
  description = "The name of the ECR repository"
}

variable "image_tag_mutability" {
  type        = string
  description = "MUTABLE or IMMUTABLE tag policy for the repository"
  default     = "MUTABLE"
}

variable "scan_on_push" {
  type        = bool
  description = "Enable image vulnerability scanning on push"
  default     = true
}

variable "max_image_count" {
  type        = number
  description = "Keep only the N most recent images (lifecycle policy)"
  default     = 5
}
