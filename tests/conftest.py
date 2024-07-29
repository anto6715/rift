from pathlib import Path

import pytest


@pytest.fixture
def wrong_mock_config_file(tmp_path):
    # Create a temporary configuration file for testing
    config_content = """
[Exec]
test_procedure = test_procedure_name

[Environment]
key1 = value1

[Modules]
TEST_MODULES = module1 module2
conda_env = myenv4
    """
    config_file = tmp_path / "test_config_wrong.ini"
    config_file.write_text(config_content)
    yield config_file
    config_file.unlink()


@pytest.fixture
def mock_config_file(tmp_path):
    # Create a temporary configuration file for testing
    config_content = """
[Exec]
test_procedure = test_procedure_name
modules = module1 module2
conda_env = myenv

[Environment]
key1 = value1

[GIT_mic-square]
name = mic-square
url = git@mic-square
branch = master

[GIT_CMEMS_DevOpsEnv]
name = CMEMS_DevOpsEnv
url = git@CMEMS_DevOpsEnv
branch = dev
    """
    config_file = tmp_path / "my_test.ini"
    config_file.write_text(config_content)
    yield config_file
    config_file.unlink()


@pytest.fixture
def root_rift_project():
    return Path(__file__).parent.parent
