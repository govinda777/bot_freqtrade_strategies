# Terraform configuration variables file
# Preencha estes valores com as informações adequadas para a construção da infraestrutura.

aws_region         = "us-east-1"
environment        = "development"
cluster_name       = "my-eks-cluster"
# db_password is loaded from environment variable: set TF_VAR_db_password in your environment.
allowed_cidr_blocks= ["0.0.0.0/0"]