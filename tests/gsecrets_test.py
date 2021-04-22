from mocks.gs_mock import MockSecrets
import envyconfig
from envyconfig.lib import methods
import pytest


@pytest.fixture(autouse=True)
def inject_method_loader(monkeypatch):
    def mock_configurer():
        return {'gs': lambda s: methods._gcp_secrets(MockSecrets(), s)}
    monkeypatch.setattr(methods, '_configure_gcp_secret_manager', mock_configurer)


def test_basic_gs():
    config = envyconfig.load('fixtures/basic_gs.yaml')
    assert config['bar'] == 'projects/my-project/secrets/my-secret/versions/1'


def test_nested_gs():
    config = envyconfig.load('fixtures/nested_gs.yaml')
    assert config['foo']['bar'] == 'projects/my-project/secrets/my-secret/versions/1'


def test_that_we_can_specify_a_secret_version():
    config = envyconfig.load('fixtures/basic_gs.yaml')
    assert config['foo'] == 'projects/my-project/secrets/my-secret/versions/2'
