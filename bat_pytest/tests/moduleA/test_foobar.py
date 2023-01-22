from base import BaseTest 
import pytest
import libs.aws.s3 as s3


class TestFoobar(BaseTest):

    def setup_class(cls):
        cls.s3 = s3.S3Lib()

    def test_foobar(self):
        #self.s3.list_buckets()
        pytest.fail("Not implemented")

    def test_foobar_a(self):
        pytest.fail("Not implemented")