from base import BaseTest
import pytest
import libs.aws.s3 as s3


class TestFoo(BaseTest):
    @pytest.fixture
    def s3obj(self):
        return s3.S3Lib()

    def test_foo_a(self, s3obj):
        pytest.fail("Not implemented")

    def test_foobar_ab(self):
        pytest.fail("Not implemented")
