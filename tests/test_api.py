from src.app_factory import create_app
from src.config import DEFAULT_VALUES


def _client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_api_example_returns_payload():
    client = _client()

    response = client.get("/api/example")
    data = response.get_json()

    assert response.status_code == 200
    assert isinstance(data, dict)
    assert "R1" in data
    assert "V1" in data


def test_api_calculate_returns_currents_successfully():
    client = _client()

    response = client.post("/api/calculate", json=DEFAULT_VALUES)
    data = response.get_json()

    assert response.status_code == 200
    assert data["success"] is True
    assert set(data["currents"].keys()) == {"I1", "I2", "I3"}
    assert len(data["matrix_A"]) == 3
    assert len(data["vector_B"]) == 3


def test_api_calculate_returns_400_when_missing_params():
    client = _client()

    response = client.post("/api/calculate", json={"R1": 1})
    data = response.get_json()

    assert response.status_code == 400
    assert "error" in data


def test_api_calculate_returns_415_when_content_type_is_not_json():
    client = _client()

    response = client.post("/api/calculate", data="plain text", content_type="text/plain")
    data = response.get_json()

    assert response.status_code == 415
    assert data["error"] == "Content-Type debe ser application/json"


def test_api_calculate_returns_400_when_json_is_malformed():
    client = _client()

    response = client.post("/api/calculate", data="{", content_type="application/json")
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "JSON malformado"
