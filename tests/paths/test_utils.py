import pytest

from rift.paths.utils import dot_git_parent_path


def test_dot_git_parent_path_found(tmp_path):
    # Create a temporary directory structure with a .git directory
    git_repo_path = tmp_path / "repo" / "subdir"
    git_repo_path.mkdir(parents=True)
    (git_repo_path.parent / ".git").mkdir()

    # Call the function and check the result
    assert dot_git_parent_path(git_repo_path) == git_repo_path.parent


def test_dot_git_parent_path_not_found(tmp_path):
    # Create a temporary directory structure without a .git directory
    non_git_repo_path = tmp_path / "repo" / "subdir"
    non_git_repo_path.mkdir(parents=True)

    # Call the function and check that it raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        dot_git_parent_path(non_git_repo_path)


def test_dot_git_parent_path_at_root(tmp_path):
    # Create a .git directory at the root of the temporary path
    (tmp_path / ".git").mkdir()

    # Call the function and check the result
    assert dot_git_parent_path(tmp_path) == tmp_path
