#!/usr/bin/env python3
"""
Custom Checkov policy to validate that AWS VPC has DNS hostnames enabled.
"""

from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

class VPCDnsHostnamesEnabledCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure that the VPC has DNS hostnames enabled"
        id = "CKV_VPC_01"
        supported_resources = ["aws_vpc"]
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        enable_dns_hostnames = conf.get("enable_dns_hostnames")
        if enable_dns_hostnames and isinstance(enable_dns_hostnames, list) and enable_dns_hostnames[0] == True:
            return CheckResult.PASSED
        return CheckResult.FAILED

check = VPCDnsHostnamesEnabledCheck()