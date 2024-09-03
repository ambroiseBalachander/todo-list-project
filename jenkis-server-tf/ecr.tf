resource "aws_ecr_repository" "frontend_repo" {
  name                 = "frontend-repository"  # Replace with your desired repository name
  image_tag_mutability = "MUTABLE"              # or "IMMUTABLE" based on your requirement
  image_scanning_configuration {
    scan_on_push = true                         # Enable image scanning on push
  }
}

resource "aws_ecr_repository" "backend_repo" {
  name                 = "backend-repository"  # Replace with your desired repository name
  image_tag_mutability = "MUTABLE"              # or "IMMUTABLE" based on your requirement
  image_scanning_configuration {
    scan_on_push = true                         # Enable image scanning on push
  }
}
