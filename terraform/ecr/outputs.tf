output "repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.ecr.repository_url
}

output "repository_arn" {
  description = "ECR repository ARN"
  value       = aws_ecr_repository.ecr.arn
}

output "repository_name" {
  description = "ECR repository name"
  value       = aws_ecr_repository.ecr.name
}

output "registry_id" {
  description = "AWS account ID hosting the ECR registry"
  value       = aws_ecr_repository.ecr.registry_id
}
