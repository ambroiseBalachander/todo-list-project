terraform {
  backend "s3" {
    bucket         = "devsecops-bucket41000"
    key            = "devsecops-projet/terraform.tfstate"
    region         = "eu-west-3"
    dynamodb_table = "Lock-Files"
    encrypt        = true
  }

  required_version = ">= 0.13.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 2.7.0"
    }
  }
}

provider "aws" {
  region = "eu-west-3"
}
