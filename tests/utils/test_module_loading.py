import pytest

from rift.utils.module_loading import import_string


def test_import_string():
    cls = import_string("rift.utils.module_loading.import_string")
    assert cls == import_string

    # Test exceptions raised
    with pytest.raises(ImportError):
        import_string("no_dots_in_path")
    msg = "No module named 'utils_tests"
    with pytest.raises(ImportError, match=msg):
        import_string("utils_tests.unexistent")
