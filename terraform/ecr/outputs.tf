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

output "ecr_push_user_name" {
  description = "IAM user for CI ECR push/pull (create access keys manually)"
  value       = aws_iam_user.ecr_push.name
}

output "ecr_push_user_arn" {
  description = "IAM user ARN for CI ECR push/pull"
  value       = aws_iam_user.ecr_push.arn
}
