import pytest

from rift.factories import test_case_factory
from rift.model import TestCase


@pytest.fixture
def test_case(mock_config_file) -> TestCase:
    return test_case_factory.get_test_case(mock_config_file)


def test_name(test_case):
    assert test_case.name == "my_test.ini"


def test_procedure_name(test_case):
    assert test_case.procedure_name == "test_procedure_name"


def test_get_environment(test_case):
    environment_section = test_case.environment
    assert "key1" in environment_section
    assert environment_section["key1"] == "value1"


def test_get_modules(test_case):
    modules_section = test_case.exec
    assert "module1" in modules_section.modules
    assert "module2" in modules_section.modules


def test_get_external_repo(test_case):
    repos = test_case.repositories

    # assert that repo objects have been found
    assert len(repos) > 0

    # check if git objects have been read correctly
    mic_square = repos[0]
    assert mic_square.branch == "master"
    assert mic_square.url == "git@mic-square"
    assert mic_square.name == "mic-square"

    devopsenv = repos[1]
    assert devopsenv.branch == "dev"
    assert devopsenv.url == "git@CMEMS_DevOpsEnv"
    assert devopsenv.name == "CMEMS_DevOpsEnv"
