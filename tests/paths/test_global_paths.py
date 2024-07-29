from pathlib import Path

import pytest

import rift.conf as settings
from rift.paths.global_paths_mixin import GlobalPathsMixin


class MockExecutionPaths:
    def __init__(self, execution_path: Path):
        self.execution_path = execution_path


class TestGlobalPaths(GlobalPathsMixin, MockExecutionPaths):
    pass


@pytest.fixture
def gpaths(tmp_path):
    return TestGlobalPaths(tmp_path)


def test_root(gpaths):
    assert gpaths.root.exists()

    assert (gpaths.root / "rift").exists()


def test_load_modules(gpaths):
    load_modules = gpaths.get_load_modules_script()

    assert load_modules.is_file()
    assert load_modules.name == settings.LOAD_MODULES


def test_starter(gpaths):
    starter = gpaths.get_starter()

    assert starter.is_file()
    assert starter.name == settings.RIFT_ENTRY_POINT


def test_get_shell_lib_entry_point(gpaths):
    shell_lib = gpaths.get_shell_lib_entry_point()

    assert shell_lib.is_file()
    assert shell_lib.name == settings.SHELL_UTILS
