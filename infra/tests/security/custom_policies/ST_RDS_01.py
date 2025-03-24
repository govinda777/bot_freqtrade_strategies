#!/usr/bin/env python3
"""
Custom Checkov policy to validate that AWS RDS has deletion protection enabled.
"""

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

class RDSDeletionProtectionEnabledCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that the RDS instance has deletion protection enabled"
        id = "CKV_RDS_01"
        supported_resources = ["aws_db_instance"]
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        deletion_protection = conf.get("deletion_protection")
        if deletion_protection and isinstance(deletion_protection, list) and deletion_protection[0] == True:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = RDSDeletionProtectionEnabledCheck()