import pytest

from src.decorators.error_handling import error_handling


class DummyStrategy:
    @error_handling()
    def create(self, mode):
        if mode == "missing_module":
            raise ModuleNotFoundError("No module named 'some_sdk'", name="some_sdk")
        if mode == "bad_credentials":
            raise ValueError("Did not find api_key")
        if mode == "unrelated_value_error":
            raise ValueError("totally unrelated")
        if mode == "generic":
            raise RuntimeError("boom")
        return "ok"


def test_success_passthrough():
    assert DummyStrategy().create("ok") == "ok"


def test_missing_module_becomes_actionable_runtime_error():
    with pytest.raises(RuntimeError) as exc_info:
        DummyStrategy().create("missing_module")
    assert "uv add some_sdk" in str(exc_info.value)
    assert "DummyStrategy" in str(exc_info.value)


def test_auth_shaped_value_error_becomes_clear_message():
    with pytest.raises(ValueError) as exc_info:
        DummyStrategy().create("bad_credentials")
    assert "Authetication failure" in str(exc_info.value)


def test_unrelated_value_error_is_reraised_unchanged():
    with pytest.raises(ValueError) as exc_info:
        DummyStrategy().create("unrelated_value_error")
    assert str(exc_info.value) == "totally unrelated"


def test_generic_exception_is_wrapped_with_strategy_name():
    with pytest.raises(RuntimeError) as exc_info:
        DummyStrategy().create("generic")
    assert "DummyStrategy" in str(exc_info.value)
    assert "boom" in str(exc_info.value)
