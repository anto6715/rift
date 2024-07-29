import subprocess

import pytest

from rift.core.source import download_from_github


def test_download_from_github_success(mocker, tmp_path):
    mock_run = mocker.patch("subprocess.run")
    url = "https://github.com/user/repo.git"
    branch = "main"
    dst = tmp_path / "repo"

    download_from_github(url, branch, dst)

    mock_run.assert_called_once_with(
        ["git", "clone", "-b", branch, url, dst],
        stdout=None,
        stderr=None,
        text=True,
        check=True,
    )


def test_download_from_github_called_process_error(mocker, tmp_path):
    mock_run = mocker.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "git")
    )
    mock_logging = mocker.patch("logging.exception")
    url = "https://github.com/user/repo.git"
    branch = "main"
    dst = tmp_path / "repo"

    with pytest.raises(subprocess.CalledProcessError):
        download_from_github(url, branch, dst)

    mock_run.assert_called_once_with(
        ["git", "clone", "-b", branch, url, dst],
        stdout=None,
        stderr=None,
        text=True,
        check=True,
    )
    assert mock_logging.call_count == 1


def test_download_from_github_file_exists_error(mocker, tmp_path):
    dst = tmp_path / "repo"
    dst.mkdir()

    url = "https://github.com/user/repo.git"
    branch = "main"

    with pytest.raises(FileExistsError):
        download_from_github(url, branch, dst)
