#!/usr/bin/env python3
"""
Custom Checkov policy to validate that AWS EKS cluster has logging enabled.
"""

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

class EKSLoggingEnabledCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that the EKS cluster has at least one logging type enabled"
        id = "CKV_EKS_01"
        supported_resources = ["aws_eks_cluster"]
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        # Check if enabled_cluster_log_types exists and is non-empty
        enabled_cluster_log_types = conf.get("enabled_cluster_log_types")
        if enabled_cluster_log_types and isinstance(enabled_cluster_log_types, list) and len(enabled_cluster_log_types) > 0:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = EKSLoggingEnabledCheck()