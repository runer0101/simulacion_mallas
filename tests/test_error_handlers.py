from src.app_factory import create_app


def test_not_found_handler_returns_custom_page():
    app = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    response = client.get("/ruta-inexistente")

    assert response.status_code == 404
    assert b"P\xc3\xa1gina no encontrada (Error 404)" in response.data


def test_internal_error_handler_returns_custom_page():
    app = create_app()
    app.config["TESTING"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = False

    @app.route("/boom-test")
    def boom_test():
        raise RuntimeError("boom")

    client = app.test_client()
    response = client.get("/boom-test")

    assert response.status_code == 500
    assert b"Error interno del servidor (Error 500)" in response.data
