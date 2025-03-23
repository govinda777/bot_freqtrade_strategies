resource "aws_db_subnet_group" "freqtrade" {
  count       = var.use_localstack ? 0 : 1
  name       = "freqtrade-${var.environment}"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name        = "Freqtrade DB subnet group"
    Environment = var.environment
    Terraform   = "true"
  }
}

resource "aws_security_group" "rds" {
  name        = "freqtrade-rds-${var.environment}"
  description = "Allow inbound traffic from EKS cluster to PostgreSQL"
  vpc_id      = module.vpc.vpc_id

  ingress {
    description     = "PostgreSQL from EKS"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.node_group_one.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "freqtrade-rds-sg"
    Environment = var.environment
    Terraform   = "true"
  }
}

resource "aws_db_instance" "freqtrade" {
  count                = var.use_localstack ? 0 : 1
  identifier             = "freqtrade-${var.environment}"
  allocated_storage      = 20
  engine                 = "postgres"
  engine_version         = "14.6"
  instance_class         = "db.t3.micro"
  db_name                = "freqtrade_multi"
  username               = "freqtrade_admin"
  password               = var.db_password
  db_subnet_group_name   = try(aws_db_subnet_group.freqtrade[0].name, "")
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = "default.postgres14"
  publicly_accessible    = false
  skip_final_snapshot    = true
  multi_az               = var.environment == "production" ? true : false

  tags = {
    Name        = "freqtrade-db"
    Environment = var.environment
    Terraform   = "true"
  }
}

# Cria um secret no Kubernetes com as credenciais do RDS
resource "kubernetes_secret" "rds_credentials" {
  count = var.use_localstack ? 0 : 1
  metadata {
    name      = "freqtrade-db-credentials"
    namespace = "freqtrade"
  }

  data = {
    username = aws_db_instance.freqtrade[0].username
    password = aws_db_instance.freqtrade[0].password
    host     = aws_db_instance.freqtrade[0].address
    port     = aws_db_instance.freqtrade[0].port
    dbname   = aws_db_instance.freqtrade[0].db_name
  }

  type = "Opaque"

  depends_on = [aws_db_instance.freqtrade]
}
