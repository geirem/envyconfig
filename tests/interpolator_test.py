from src.envyconfig import envyconfig


def test_multiple_colons():
    config = envyconfig.load('tests/fixtures/complex.yaml')
    assert config['foo'] == 'default:with:'
