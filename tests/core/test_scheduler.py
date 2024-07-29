import psutil
import pytest
from unittest.mock import patch, MagicMock
from rift.core import scheduler


# Replace 'your_script_name' with the actual name of your script file.


@pytest.fixture(scope="session", autouse=True)
def mock_process():
    mock = MagicMock(spec=psutil.Process)
    mock.return_value.pid = 12345
    mock.name = "mocked_process"
    return mock


@pytest.fixture
def mock_safe_kill():
    return MagicMock()


def test_kill_process_with_child(mock_safe_kill, mock_process):
    root_pid = 12345
    x = mock_process.pid
    # with return_value access the value that the mock will return when it's called
    mock_process_instance = mock_process
    # mock_process_instance.pid = root_pid

    # Assuming you want to mock the children method as well
    mock_process_instance.children.return_value = []

    with patch("rift.core.scheduler.safe_kill", mock_safe_kill):
        with patch("psutil.Process", mock_process):
            scheduler.kill_process_with_child(root_pid)

    mock_process_instance.return_value.children.assert_called_once_with(recursive=True)
    mock_safe_kill.assert_called_once_with(root_pid)


@patch("psutil.Process")
def test_kill_process_with_child_exception_handling(mock_process, mock_safe_kill):
    root_pid = 12345
    mock_process.side_effect = psutil.NoSuchProcess("Mocked error")
    mock_process.pid = root_pid

    with patch("rift.core.scheduler.safe_kill", mock_safe_kill):
        scheduler.kill_process_with_child(root_pid)

    mock_process.children.assert_not_called()
    mock_safe_kill.assert_not_called()


@patch("psutil.Process")
def test_safe_kill(mock_process):
    pid = 54321
    mock_process.return_value.wait.side_effect = psutil.TimeoutExpired("Mocked timeout")

    with patch("psutil.Process", return_value=mock_process):
        scheduler.safe_kill(pid)

    mock_process.kill.assert_called_once()
    mock_process.wait.assert_called_once_with(timeout=5)
    mock_process.wait.side_effect = None  # Reset side effect for subsequent tests


def test_safe_kill_exceptions():
    pid = 54321
    with patch("psutil.Process", side_effect=psutil.NoSuchProcess("Mocked error")):
        scheduler.safe_kill(pid)

    with patch("psutil.Process", side_effect=psutil.AccessDenied("Mocked error")):
        scheduler.safe_kill(pid)

    with patch("psutil.Process", side_effect=Exception("Mocked error")):
        scheduler.safe_kill(pid)


if __name__ == "__main__":
    pytest.main()
