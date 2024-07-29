from rift.factories.test_case_factory import get_test_case
from rift.model import TestCase


def test_get_test_case(mock_config_file):
    test_case = get_test_case(mock_config_file)

    assert isinstance(test_case, TestCase)


def test_get_test_case_repos(mock_config_file):
    test_case = get_test_case(mock_config_file)

    assert isinstance(test_case, TestCase)
    assert test_case.repositories is not None
    assert len(test_case.repositories) > 0
