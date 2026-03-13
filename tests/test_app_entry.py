from app import _parse_env_bool


def test_parse_env_bool_accepts_truthy_values():
    assert _parse_env_bool("true") is True
    assert _parse_env_bool("TRUE") is True
    assert _parse_env_bool("1") is True
    assert _parse_env_bool("yes") is True
    assert _parse_env_bool("on") is True


def test_parse_env_bool_rejects_falsy_values():
    assert _parse_env_bool("false") is False
    assert _parse_env_bool("0") is False
    assert _parse_env_bool("off") is False
    assert _parse_env_bool("no") is False
    assert _parse_env_bool("") is False
