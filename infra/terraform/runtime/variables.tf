variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "pomodoro-quest"
}
variable "environment" {
  type    = string
  default = "dev"
}
variable "owner" {
  type    = string
  default = "Andre Santos"
}

# App
variable "container_port" {
  type    = number
  default = 8000
}
variable "health_path" {
  type    = string
  default = "/api/health/ready"
}

# ECR image to run
variable "container_image" {
  type        = string
  description = "Full image URI (e.g., 792025037142.dkr.ecr.us-east-1.amazonaws.com/pomodoro-quest:latest)"
}

# Fargate sizing (keep minimal)
variable "task_cpu" {
  type    = number
  default = 256  # 0.25 vCPU
}
variable "task_memory" {
  type    = number
  default = 512  # 0.5 GB
}
variable "desired_count" {
  type    = number
  default = 1
}