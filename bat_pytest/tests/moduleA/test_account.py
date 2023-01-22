from base import BaseTest
import pytest
import libs.aws.s3 as s3


class TestAccount(BaseTest):

    def setup_method(self):
        self.obj = s3.S3Lib()

    def test_foo_account(self):
        """Test description is mandatory"""
        pytest.fail("Not implemented")

    def test_foobar_account(self):
        pytest.fail("Not implemented")
