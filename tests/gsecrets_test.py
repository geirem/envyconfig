from mocks.gs_mock import MockSecrets
from src.envyconfig import envyconfig
import pytest

from src.envyconfig.methods import _gsecrets, _configure_secret_manager
from src.envyconfig import methods


@pytest.fixture(autouse=True)
def inject_method_loader(monkeypatch):
    def mock_configurer():
        return {'gs': lambda s: _gsecrets(MockSecrets(), s)}
    monkeypatch.setattr(methods, '_configure_secret_manager', mock_configurer)


def test_basic_gs():
    config = envyconfig.load('fixtures/basic_gs.yaml', configure_methods=['gs'])
    assert config['bar'] == 'projects/my-project/secrets/my-secret/versions/1'


def test_nested_gs():
    config = envyconfig.load('fixtures/nested_gs.yaml', configure_methods=['gs'])
    assert config['foo']['bar'] == 'projects/my-project/secrets/my-secret/versions/1'


def test_that_we_can_specify_a_secret_version():
    config = envyconfig.load('fixtures/basic_gs.yaml', configure_methods=['gs'])
    assert config['foo'] == 'projects/my-project/secrets/my-secret/versions/2'
