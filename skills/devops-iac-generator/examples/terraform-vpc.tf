# Example: Terraform VPC module
# Input: iac_tool=terraform, cloud_provider=aws, resources=[vpc, subnets]

variable "environment" {
  type = string
  description = "Environment (dev/staging/prod)"
}

variable "vpc_cidr" {
  type = string
  default = "10.0.0.0/16"
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = "${var.environment}-vpc"
    Environment = var.environment
  }
}

output "vpc_id" {
  value = aws_vpc.main.id
  description = "VPC ID for resource references"
}
