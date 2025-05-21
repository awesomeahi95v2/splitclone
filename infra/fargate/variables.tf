variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}

variable "docker_image_url" {
  description = "Full ECR image URI"
  type        = string
}

variable "container_port" {
  description = "Port your Flask app listens on"
  default     = 5000
}

variable "app_name" {
  description = "Name of the ECS app/service"
  default     = "splitclone"
}

variable "cpu" {
  description = "CPU units for Fargate task"
  default     = 256
}

variable "memory" {
  description = "Memory (MB) for Fargate task"
  default     = 512
}

variable "desired_count" {
  description = "Number of running containers"
  default     = 1
}
