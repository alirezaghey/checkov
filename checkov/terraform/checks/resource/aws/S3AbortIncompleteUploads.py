from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.models.enums import CheckCategories, CheckResult


class S3AbortIncompleteUploads(BaseResourceCheck):
    def __init__(self):
        """
        If you don't set this value in a lifecycle configuration you'll end up paying for s3
        resources you never could use
        """
        name = "Ensure S3 lifecycle configuration sets period for aborting failed uploads"
        id = "CKV_AWS_300"
        supported_resources = ('aws_s3_bucket_lifecycle_configuration',)
        categories = (CheckCategories.GENERAL_SECURITY,)
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        self.evaluated_keys = ["rule"]
        rules = conf.get("rule")
        if rules and isinstance(rules, list):
            for idx_rule, rule in enumerate(rules):
                if not rule.get("abort_incomplete_multipart_upload"):
                    self.evaluated_keys = [f"rule/[{idx_rule}]/"]
                    return CheckResult.FAILED
            return CheckResult.PASSED
        return CheckResult.FAILED


check = S3AbortIncompleteUploads()
