from src.app_factory import create_app


def _client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_circuito_png_returns_image_for_valid_input():
    client = _client()

    response = client.get("/circuito.png?R1=1.2&V1=220")

    assert response.status_code == 200
    assert response.content_type == "image/png"
    assert len(response.data) > 0


def test_circuito_png_returns_400_for_non_numeric_value():
    client = _client()

    response = client.get("/circuito.png?R1=abc")

    assert response.status_code == 400
    assert b"R1: Debe ser un n\xc3\xbamero v\xc3\xa1lido" in response.data


def test_circuito_png_returns_400_for_out_of_range_value():
    client = _client()

    response = client.get("/circuito.png?R1=0")

    assert response.status_code == 400
    assert b"R1: Debe ser un valor positivo" in response.data
