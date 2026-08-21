resource "aws_iam_user" "ecr_push" {
  name = "${var.username}-${var.repo}-${var.environment}-ecr-push"
}

resource "aws_iam_user_policy" "ecr_push" {
  name = "${var.username}-${var.repo}-${var.environment}-ecr-push"
  user = aws_iam_user.ecr_push.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "EcrAuthToken"
        Effect   = "Allow"
        Action   = ["ecr:GetAuthorizationToken"]
        Resource = "*"
      },
      {
        Sid    = "EcrPushPull"
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:DescribeRepositories",
          "ecr:DescribeImages",
          "ecr:ListImages",
        ]
        Resource = aws_ecr_repository.ecr.arn
      }
    ]
  })
}
