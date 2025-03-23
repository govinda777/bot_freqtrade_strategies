module "eks" {
  count = var.use_localstack ? 0 : 1
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 18.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.23"

  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Gerenciamento de nós do EKS
  eks_managed_node_group_defaults = {
    ami_type               = "AL2_x86_64"
    disk_size              = 50
    instance_types         = ["t3.medium"]
    vpc_security_group_ids = [aws_security_group.node_group_one.id]
  }

  eks_managed_node_groups = {
    freqtrade_nodes = {
      min_size     = 2
      max_size     = 5
      desired_size = 3

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = var.environment
        Application = "freqtrade"
      }

      tags = {
        Environment = var.environment
        Terraform   = "true"
        Application = "freqtrade"
      }
    }
  }

  tags = {
    Environment = var.environment
    Terraform   = "true"
    Application = "freqtrade"
  }
}

resource "aws_security_group" "node_group_one" {
  name_prefix = "node_group_one"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = [
      "10.0.0.0/8",
    ]
  }

  tags = {
    Environment = var.environment
    Terraform   = "true"
    Application = "freqtrade"
  }
}
