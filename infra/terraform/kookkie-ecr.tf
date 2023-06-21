
locals {
  keep-only-a-few-policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Keep only the latest tagged image",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 5
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}


resource "aws_ecr_lifecycle_policy" "backend-policy" {
  repository = aws_ecr_repository.backend.name
  policy = local.keep-only-a-few-policy
}

resource "aws_ecr_repository" "backend" {
  name                 = "qwan/kookkie-backend"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Infra = "kookkie"
  }
}


resource "aws_ecr_lifecycle_policy" "backup-policy" {
  repository = aws_ecr_repository.backup.name
  policy = local.keep-only-a-few-policy
}

resource "aws_ecr_repository" "backup" {
  name                 = "qwan/kookkie-backup"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Infra = "kookkie"
  }
}


resource "aws_ecr_lifecycle_policy" "frontend-policy" {
  repository = aws_ecr_repository.frontend.name
  policy = local.keep-only-a-few-policy
}

resource "aws_ecr_repository" "frontend" {
  name                 = "qwan/kookkie-frontend"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Infra = "kookkie"
  }
}


resource "aws_ecr_lifecycle_policy" "proxy-policy" {
  repository = aws_ecr_repository.proxy.name
  policy = local.keep-only-a-few-policy
}

resource "aws_ecr_repository" "proxy" {
  name                 = "qwan/kookkie-proxy"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Infra = "kookkie"
  }
}


resource "aws_ecr_lifecycle_policy" "cloudwatch-agent-policy" {
  repository = aws_ecr_repository.cloudwatch-agent.name
  policy = local.keep-only-a-few-policy
}

resource "aws_ecr_repository" "cloudwatch-agent" {
  name                 = "qwan/kookkie-cloudwatch-agent"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Infra = "kookkie"
  }
}
