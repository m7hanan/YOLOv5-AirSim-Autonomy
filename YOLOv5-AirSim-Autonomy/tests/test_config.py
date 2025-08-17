import config

def test_config_defaults():
    assert isinstance(config.WAYPOINTS, list)
    assert config.DRONE_HOST == "127.0.0.1"
