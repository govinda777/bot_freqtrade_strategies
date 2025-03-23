output "cluster_id" {
  description = "ID do cluster EKS"
  value       = try(module.eks[0].cluster_id, "")
}

output "cluster_endpoint" {
  description = "Endpoint do cluster EKS"
  value       = try(module.eks[0].cluster_endpoint, "")
}

output "cluster_security_group_id" {
  description = "ID do security group do cluster EKS"
  value       = try(module.eks[0].cluster_security_group_id, "")
}

output "kubectl_config" {
  description = "Comando para configurar o kubectl"
  value       = "aws eks update-kubeconfig --region ${var.aws_region} --name ${try(module.eks[0].cluster_id, "")}"
}

output "rds_endpoint" {
  description = "Endpoint da instância RDS"
  value       = length(aws_db_instance.freqtrade) > 0 ? aws_db_instance.freqtrade[0].address : ""
}

output "rds_port" {
  description = "Porta da instância RDS"
  value       = length(aws_db_instance.freqtrade) > 0 ? aws_db_instance.freqtrade[0].port : 0
}

output "rds_username" {
  description = "Usuário da instância RDS"
  value       = length(aws_db_instance.freqtrade) > 0 ? aws_db_instance.freqtrade[0].username : ""
}

output "rds_database_name" {
  description = "Nome do banco de dados RDS"
  value       = length(aws_db_instance.freqtrade) > 0 ? aws_db_instance.freqtrade[0].db_name : ""
}
