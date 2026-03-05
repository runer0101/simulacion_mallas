from src.config import DEFAULT_VALUES
from src.validators.inputs import parse_form_data, validate_api_payload, validate_parameters


def test_validate_parameters_accepts_valid_payload():
    validate_parameters(DEFAULT_VALUES.copy())


def test_validate_parameters_rejects_invalid_resistance():
    params = DEFAULT_VALUES.copy()
    params["R1"] = 0

    try:
        validate_parameters(params)
        assert False, "Expected ValueError for non-positive resistance"
    except ValueError as exc:
        assert "R1" in str(exc)


def test_parse_form_data_parses_commas_and_validates():
    form_data = {"R1": "1,5", "V1": "220"}
    vals, error = parse_form_data(form_data, DEFAULT_VALUES)

    assert error is None
    assert vals["R1"] == 1.5
    assert vals["V1"] == 220.0


def test_validate_api_payload_detects_missing_fields():
    payload, error = validate_api_payload({"R1": 1.0})

    assert payload is None
    assert error is not None
    assert "Parámetros faltantes" in error


def test_validate_api_payload_returns_numeric_params():
    raw = {key: str(value) for key, value in DEFAULT_VALUES.items()}
    payload, error = validate_api_payload(raw)

    assert error is None
    assert payload is not None
    assert all(isinstance(v, float) for v in payload.values())
