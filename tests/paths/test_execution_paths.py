from pathlib import Path

import pytest

from rift.paths.execution_paths_mixin import ExecutionPathsMixin


class MockExecutionPaths:
    def __init__(self, execution_path: Path):
        self.execution_path = execution_path


class TestExecutionPaths(ExecutionPathsMixin, MockExecutionPaths):
    pass


@pytest.fixture
def execution_paths(tmp_path):
    return TestExecutionPaths(tmp_path)


def test_execution_paths(execution_paths):
    assert execution_paths.get_work_dir() == execution_paths.execution_path / "work"
    assert execution_paths.get_log_dir() == execution_paths.execution_path / "log"
    assert execution_paths.get_out_dir() == execution_paths.execution_path / "out"
