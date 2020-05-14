from src.envyconfig import envyconfig


def test_basic():
    config = envyconfig.load('fixtures/basic.yaml', configure_methods=[])
    assert config['foo'] == 'bar'


def test_nested():
    config = envyconfig.load('fixtures/basic_nested.yaml', configure_methods=[])
    assert config['foo']['bar'] == 'baz'


def test_flattened():
    config = envyconfig.load('fixtures/basic_nested.yaml', configure_methods=[], flatten=True)
    assert config['bar'] == 'baz'
