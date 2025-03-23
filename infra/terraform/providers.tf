terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }

    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }

    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }

    cloudinit = {
      source  = "hashicorp/cloudinit"
      version = "~> 2.3"
    }
  }
}
 
locals {
  is_development              = var.environment == "development"
  dummy_ca = <<EOF
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAO31zMRyH3RlMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAlVTMRYwFAYDVQQIDA1DYWxpZm9ybmlhMRYwFAYDVQQKDA1NeSBDb21wYW55
IENBMB4XDTE5MTEwMTAwMDAwMFoXDTIxMTEwMTAwMDAwMFowRTELMAkGA1UEBhMC
VVMxFjAUBgNVBAgMDUNhbGlmb3JuaWExFjAUBgNVBAoMDU15IENvbXBhbnkgQ0Ew
ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCw+MpX3W4Mv7E6c9UaDxCs
gTnZ04q5KSRhru66SbBVlS0xQgb0T8nT8c7+gBzUmXEFHWv/Vo5+7DmP4wgF9uHe
iVt2P08CkY1F9FZT9oG+eXGJJ4ivJdn6iLWtY6NnteS6IY8ENzTq8P5A5QdcFouY
3j8N3aj7sJ8uWr7JitQG6xZ2W9WcZgPvLZrh3XkXozM5XjXs28uma7WmQ3bpQj/h
0SAwI0TRoWGF0c6Oy2t3CrE1RrLnxztW9REHig7I4VlypQO4BScxUoDjZlMEzV0Z
6RzH2IHw7lDi2XHQ5RqBZkZ0+5KxJqM3j0tJgPRE37uB0qmI/5hE1Sw4kkqz3y9v
AgMBAAGjUzBRMB0GA1UdDgQWBBTKNxg/1Bsg0MBhVIJFPKpsRydCdjAfBgNVHSME
GDAWgBTKNxg/1Bsg0MBhVIJFPKpsRydCdjAPBgNVHRMBAf8EBTADAQH/MA0GCSqG
SIb3DQEBCwUAA4IBAQA7Pu5IxZZlZB0Xc/C5VXKv9j56kcjO/5YxIR3s0uDyxqL+
KblE2d5n40/VtqTjSyV5vKUmp8zk5HVw3k50iK4IYIYQ8XWf2IY1/kJKBQvHz4VX
hE7E7R5NkChPtZc3xFJXjkP1Df0mXk+0gB7n8IlgkOWP9LO/jI6GWXRJ5H8Ou7xP
WPQmDoFg9wYI0B87fnqGEeN6Gl9fPAAmJ6JXG3G8UriE9dFslv9f6Ih6vZT3ADjr
Ai4z6RkXRJ3sr6zyTjQk8KnePMIEZkA6aZ5R9lkg/MEpFvGfPF0x/YJd0EZQF5LO
ro76bCdyz6J09L1TeuCqKeSdY/mb1Ww2TSI8Vwd2
-----END CERTIFICATE-----
EOF
  eks_cluster_endpoint        = local.is_development ? "http://localhost:4566/eks" : data.aws_eks_cluster.cluster[0].endpoint
  eks_cluster_ca_certificate  = local.is_development ? local.dummy_ca : base64decode(data.aws_eks_cluster.cluster[0].certificate_authority[0].data)
  eks_cluster_token           = local.is_development ? "dummy-token" : data.aws_eks_cluster_auth.cluster[0].token
}

provider "aws" {
  region       = var.aws_region
  access_key   = local.is_development ? "test" : null
  secret_key   = local.is_development ? "test" : null
  profile      = local.is_development ? null : "admin"
  skip_credentials_validation = local.is_development ? true : false
  dynamic "endpoints" {
    for_each = local.is_development ? [1] : []
    content {
      ec2            = "http://localhost:4566"
      sts            = "http://localhost:4566"
      iam            = "http://localhost:4566"
      rds            = "http://localhost:4566"
      cloudwatchlogs = "http://localhost:4566"
    }
  }
}

provider "kubernetes" {
  host                   = local.eks_cluster_endpoint
  cluster_ca_certificate = trimspace(local.eks_cluster_ca_certificate)
  token                  = local.eks_cluster_token
}

provider "helm" {
  kubernetes {
    host                   = local.eks_cluster_endpoint
    cluster_ca_certificate = trimspace(local.eks_cluster_ca_certificate)
    token                  = local.eks_cluster_token
  }
}

data "aws_eks_cluster" "cluster" {
  count = local.is_development ? 0 : 1
  name  = var.cluster_name
}

data "aws_eks_cluster_auth" "cluster" {
  count = local.is_development ? 0 : 1
  name  = var.cluster_name
}
