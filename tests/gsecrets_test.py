from mocks.gs_mock import MockSecrets
from src import envyconfig, methods
import pytest

from src import _gcp_secrets


@pytest.fixture(autouse=True)
def inject_method_loader(monkeypatch):
    def mock_configurer():
        return {'gs': lambda s: _gcp_secrets(MockSecrets(), s)}
    monkeypatch.setattr(methods, '_configure_gcp_secret_manager', mock_configurer)


def test_basic_gs():
    config = envyconfig.load('tests/fixtures/basic_gs.yaml')
    assert config['bar'] == 'projects/my-project/secrets/my-secret/versions/1'


def test_nested_gs():
    config = envyconfig.load('tests/fixtures/nested_gs.yaml')
    assert config['foo']['bar'] == 'projects/my-project/secrets/my-secret/versions/1'


def test_that_we_can_specify_a_secret_version():
    config = envyconfig.load('tests/fixtures/basic_gs.yaml')
    assert config['foo'] == 'projects/my-project/secrets/my-secret/versions/2'
