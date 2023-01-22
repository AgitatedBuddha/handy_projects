from base import BaseTest
import pytest
import libs.aws.s3 as s3


class TestModuleBFoo(BaseTest):

    def setup_method(self):
        self.obj = s3.S3Lib()

    def test_foo(self):
        """Test description is mandatory"""
        pytest.fail("Not implemented")

