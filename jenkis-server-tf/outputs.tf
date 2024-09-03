output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_id" {
  description = "Public Subnet ID"
  value       = aws_subnet.public.id
}

output "jenkins_instance_id" {
  description = "Jenkins EC2 Instance ID"
  value       = aws_instance.jenkins.id
}

output "jenkins_public_ip" {
  description = "Public IP of Jenkins server"
  value       = aws_instance.jenkins.public_ip
}

# Output the repository URLs
output "frontend_repository_url" {
  value = aws_ecr_repository.frontend_repo.repository_url
}

output "backend_repository_url" {
  value = aws_ecr_repository.backend_repo.repository_url
}