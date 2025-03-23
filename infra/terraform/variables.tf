variable "use_localstack" {
  description = "Whether to use LocalStack (true) to disable unsupported AWS services resources creation."
  type        = bool
  default     = false
}

variable "environment" {
  description = "Deployment environment (e.g. development, production)"
  type        = string
  default     = "development"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "freqtrade-cluster"
}
variable "aws_region" {
  description = "AWS region to use"
  type        = string
}

variable "db_password" {
  description = "Database password for the database"
  type        = string
  sensitive   = true
}

variable "allowed_cidr_blocks" {
  description = "List of allowed CIDR blocks"
  type        = list(string)
}