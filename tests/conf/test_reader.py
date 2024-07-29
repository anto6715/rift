import json
import tempfile
from pathlib import Path
from typing import Callable, Dict, List
from unittest.mock import Mock

import pytest

from rift.conf import read_config
from rift.conf import reader


def get_temporary_file(ext: str) -> Path:
    f = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
    return Path(f.name)


@pytest.fixture
def mock_read_json():
    return Mock(return_value={"type": "json"})


@pytest.fixture
def mock_read_yaml():
    return Mock(return_value={"type": "yaml"})


@pytest.fixture
def mock_read_ini():
    return Mock(return_value={"type": "ini"})


@pytest.fixture
def mock_readers(
    mock_read_json, mock_read_ini, mock_read_yaml
) -> Dict[Callable, List[str]]:
    return {
        mock_read_json: [".json", ".jsn"],
        mock_read_yaml: [".yaml", ".yml"],
        mock_read_ini: [".ini"],
    }


def test_read_config_unsupported_extension(
    monkeypatch, mock_readers, mock_read_json, mock_read_ini, mock_read_yaml
):
    monkeypatch.setattr("rift.conf.readers", mock_readers)
    f = get_temporary_file(".nc")
    with pytest.raises(ValueError):
        read_config(f)


def test_read_config_json(
    monkeypatch, mock_readers, mock_read_json, mock_read_ini, mock_read_yaml
):
    monkeypatch.setattr("rift.conf.readers", mock_readers)
    f = get_temporary_file(".json")
    assert read_config(f) == {"type": "json"}
    mock_read_json.assert_called_once()
    mock_read_yaml.assert_not_called()
    mock_read_ini.assert_not_called()


def test_read_config_ini(
    monkeypatch, mock_readers, mock_read_json, mock_read_ini, mock_read_yaml
):
    monkeypatch.setattr("rift.conf.readers", mock_readers)
    f = get_temporary_file(".ini")
    assert read_config(f) == {"type": "ini"}
    mock_read_json.assert_not_called()
    mock_read_yaml.assert_not_called()
    mock_read_ini.assert_called_once()


def test_read_config_yaml(
    monkeypatch, mock_readers, mock_read_json, mock_read_ini, mock_read_yaml
):
    monkeypatch.setattr("rift.conf.readers", mock_readers)
    f = get_temporary_file(".yaml")
    assert read_config(f) == {"type": "yaml"}
    mock_read_json.assert_not_called()
    mock_read_yaml.assert_called_once()
    mock_read_ini.assert_not_called()

    # reset previous call
    mock_read_yaml.reset_mock()

    f = get_temporary_file(".yml")
    assert read_config(f) == {"type": "yaml"}
    mock_read_json.assert_not_called()
    mock_read_yaml.assert_called_once()
    mock_read_ini.assert_not_called()


def test_read_json():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        # Write some JSON content to the file
        json_content = {"key": "value", "number": 42}
        temp_file.write(json.dumps(json_content).encode())

    # Ensure the file is properly closed
    temp_file.close()

    # Call the function with the Path object
    result = reader.read_json(temp_path)

    # Verify the result
    assert result == json_content

    # Clean up the temporary file
    temp_path.unlink()


def test_read_ini():
    # Create a temporary INI file
    with tempfile.NamedTemporaryFile(suffix=".ini", delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        # Write some INI content to the file
        temp_file.write(
            b"[Section1]\nkey1 = value1\nkey2 = value2\n\n[Section2]\nkey3 = value3\n"
        )

    # Ensure the file is properly closed
    temp_file.close()

    # Call the function with the Path object
    result = reader.read_ini(temp_path)

    # Verify the result
    expected_result = {"key1": "value1", "key2": "value2", "key3": "value3"}
    assert result == expected_result

    # Clean up the temporary file
    temp_path.unlink()


