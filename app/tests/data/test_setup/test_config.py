import pytest
from config import DevelopmentConfig, ProductionConfig, TestingConfig, config, load_config


def test_prod_config():
    prod_config = ProductionConfig()
    assert prod_config.ENV == 'deployed'
    assert not prod_config.DEBUG


def test_dev_config():
    dev_config = DevelopmentConfig()
    assert dev_config.ENV == 'local'
    assert dev_config.DEBUG


def test_actual_config():
    assert config.ENV == 'test'
    assert config.DEBUG


def test_load_config_dev(monkeypatch):
    monkeypatch.setenv('ENV', 'local')
    config = load_config()
    assert isinstance(config, DevelopmentConfig)


def test_load_config_test(monkeypatch):
    monkeypatch.setenv('ENV', 'test')
    config = load_config()
    assert isinstance(config, TestingConfig)


def test_load_config_prod(monkeypatch):
    monkeypatch.setenv('ENV', 'deployed')
    config = load_config()
    assert isinstance(config, ProductionConfig)


def test_load_config_default(monkeypatch):
    monkeypatch.delenv('ENV', raising=False)
    config = load_config()
    assert isinstance(config, DevelopmentConfig)


def test_load_config_invalid(monkeypatch):
    monkeypatch.setenv('ENV', 'invalid')
    with pytest.raises(Exception) as excinfo:
        load_config()
    assert 'Incorrect value for environment variable ENV' in str(excinfo.value)
