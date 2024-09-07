variable "region" {
  description = "AWS Region"
  default     = "eu-west-3"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public Subnet CIDR block"
  default     = "10.0.1.0/24"
}

variable "private_subnet_cidr" {
  description = "Private Subnet CIDR block"
  default     = "10.0.2.0/24"
}

variable "instance_type" {
  description = "EC2 instance type for Jenkins"
  default     = "t2.xlarge"
}

variable "key_name" {
  description = "Key pair name for EC2 instance"
  default     = "my-jenkins-key"
}

variable "allowed_ip" {
  description = "Allowed IP for SSH and Jenkins access"
  default     = "0.0.0.0/0" # Replace with your IP or CIDR
}
