variable "aws_region" {
  description = "Região AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Ambiente (desenvolvimento, staging, produção)"
  type        = string
  default     = "development"
}

variable "cluster_name" {
  description = "Nome do cluster EKS"
  type        = string
  default     = "freqtrade-cluster"
}

variable "db_password" {
  description = "Senha para o banco de dados RDS"
  type        = string
  sensitive   = true
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks permitidos para conectar ao cluster"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
