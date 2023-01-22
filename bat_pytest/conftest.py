# conftest.py
import pytest
import sys
import logging
import allure


@pytest.fixture
def db():
    # connect db
    yield
    # close db


def pytest_collection_modifyitems(items):
    for item in items:
        allure.suite(item.parent.name)


def pytest_configure(config):
    allure.suite('test_class')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler("ieg_bat.log"),
            logging.StreamHandler(sys.stdout)
        ])

def pytest_runtest_logstart(nodeid, location):
    logger = logging.getLogger(__name__)
    filename, class_name, method_name = nodeid.split("::")
    logger.info(f"Test class: {class_name} TestCase: {method_name}")


def pytest_unconfigure(config):
    allure.suite(None)
    logging.shutdown()
