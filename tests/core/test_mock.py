from pathlib import Path

from rift.core import mock

TEST_CASE_NAME = "my_test.ini"
TEST_PROCEDURE_NAME = "tests/my_test"


def test_initialize_test_case(tmp_path):
    cwd = Path.cwd()
    test_procedure = cwd / TEST_PROCEDURE_NAME
    to_init = tmp_path / TEST_CASE_NAME
    mock.initialize_test_case(to_init)

    assert to_init.exists()
    assert test_procedure.exists()

    to_init.unlink()
    for f in test_procedure.iterdir():
        f.unlink()
    test_procedure.rmdir()
