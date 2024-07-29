from pathlib import Path

import pytest

import rift.conf as settings
from rift.paths.test_case_paths_mixin import TestCasePathsMixin


class MockExecutionPaths:
    pass


class TestGlobalPaths(TestCasePathsMixin, MockExecutionPaths):
    pass


@pytest.fixture
def test_case_paths():
    return TestGlobalPaths()


@pytest.fixture
def cwd():
    return Path.cwd()


def test_get_source(root_rift_project, test_case_paths):
    assert root_rift_project == test_case_paths.get_source_path()


def test_get_tests_base_path(cwd, test_case_paths):
    assert test_case_paths.get_tests_base_path() == cwd / settings.TESTS_BASE_DIR


def test_get_test_implementation_path(cwd, test_case_paths):
    procedure_name = "mock_test"
    assert (
        test_case_paths.get_test_implementation_path(procedure_name)
        == cwd / settings.TESTS_BASE_DIR / procedure_name
    )


def test_get_test_entry_point(cwd, test_case_paths):
    procedure_name = "mock_test"
    assert (
        test_case_paths.get_test_entry_point(procedure_name)
        == cwd / settings.TESTS_BASE_DIR / procedure_name / settings.TEST_ENTRY_POINT
    )
