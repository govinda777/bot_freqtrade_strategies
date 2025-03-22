output "cluster_id" {
  description = "ID do cluster EKS"
  value       = module.eks.cluster_id
}

output "cluster_endpoint" {
  description = "Endpoint do cluster EKS"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "ID do security group do cluster EKS"
  value       = module.eks.cluster_security_group_id
}

output "kubectl_config" {
  description = "Comando para configurar o kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_id}"
}

output "rds_endpoint" {
  description = "Endpoint da instância RDS"
  value       = aws_db_instance.freqtrade.address
}

output "rds_port" {
  description = "Porta da instância RDS"
  value       = aws_db_instance.freqtrade.port
}

output "rds_username" {
  description = "Usuário da instância RDS"
  value       = aws_db_instance.freqtrade.username
}

output "rds_database_name" {
  description = "Nome do banco de dados RDS"
  value       = aws_db_instance.freqtrade.db_name
}
