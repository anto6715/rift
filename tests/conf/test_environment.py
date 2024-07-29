import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from rift.conf import environment


@pytest.fixture
def mock_logger():
    with patch("logging.getLogger", return_value=MagicMock()) as mock:
        yield mock


@pytest.mark.parametrize(
    "test_dict, expected_env",
    [
        ({"VAR1": "value1", "VAR2": "value2"}, {"VAR1": "value1", "VAR2": "value2"}),
        ({}, {}),  # Test with an empty dictionary
        ({"null": None}, {}),  # Test with an empty dictionary
    ],
)
def test_export_dict(test_dict, expected_env, mock_logger):
    with patch.dict(os.environ, clear=True):
        environment.export_dict(test_dict)
        assert os.environ == expected_env


@pytest.mark.parametrize(
    "env_path, path_to_add, expected_path",
    [
        ("/ENV_PATH", Path("/path1/to/add"), "/ENV_PATH:/path1/to/add"),
        ("", Path("/new/path"), ":/new/path"),
    ],
)
def test_add_to_path_success(env_path, path_to_add, expected_path, monkeypatch):
    with patch.dict(os.environ, {"PATH": env_path}):
        environment.add_to_path(path_to_add)
        assert os.environ["PATH"] == expected_path


def test_get_global_environment_value(monkeypatch):
    monkeypatch.setitem(os.environ, "MY_VAR", "value")
    result = environment.evaluate_str_with_bash("${MY_VAR}")
    assert result == "value"

    result = environment.evaluate_str_with_bash('my_${TEST:-"test"}')
    assert result == "my_test"


def test_get_global_environment_value_unbound_variable(monkeypatch):
    with pytest.raises(ValueError):
        _ = environment.evaluate_str_with_bash("${MY_VAR}")
