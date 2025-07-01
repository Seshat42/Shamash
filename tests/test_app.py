from server.app import create_app


def test_app_includes_routes():
    app = create_app()
    paths = [route.path for route in app.router.routes]
    assert "/auth/login" in paths
    assert "/stream/ping" in paths
    assert "/metadata/sync" in paths
