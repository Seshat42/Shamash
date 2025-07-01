from server.config import CONFIG, load_config


def test_config_loads():
    assert "server" in CONFIG
    cfg = load_config()
    assert cfg["server"]["port"] == 8000
