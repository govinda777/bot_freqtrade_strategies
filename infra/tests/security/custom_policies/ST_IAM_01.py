#!/usr/bin/env python3
"""
Custom Checkov policy to validate that AWS IAM Role's assume_role_policy does not contain wildcard actions.
This policy parses the assume_role_policy JSON and fails if any statement allows "*" as an action.
"""

import json
from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

class IAMRoleNoWildcardActionCheck(BaseResourceCheck):
    def __init__(self):
        name = "Ensure AWS IAM Role's assume_role_policy does not allow wildcard actions"
        id = "CKV_IAM_01"
        supported_resources = ["aws_iam_role"]
        categories = [CheckCategories.SECURITY]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        policy = conf.get("assume_role_policy")
        if policy and isinstance(policy, list):
            try:
                parsed_policy = json.loads(policy[0])
                statements = parsed_policy.get("Statement", [])
                for statement in statements:
                    action = statement.get("Action")
                    if action:
                        if isinstance(action, list):
                            if "*" in action:
                                return CheckResult.FAILED
                        elif isinstance(action, str):
                            if action.strip() == "*":
                                return CheckResult.FAILED
                return CheckResult.PASSED
            except Exception:
                return CheckResult.FAILED
        return CheckResult.FAILED

check = IAMRoleNoWildcardActionCheck()