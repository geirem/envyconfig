from src.envyconfig import envyconfig


def test_basic():
    config = envyconfig.load('fixtures/basic.yaml')
    assert config['foo'] == 'bar'


def test_nested():
    config = envyconfig.load('fixtures/basic_nested.yaml')
    assert config['foo']['bar'] == 'baz'


def test_flattened():
    config = envyconfig.load('fixtures/basic_nested.yaml', flatten=True)
    assert config['bar'] == 'baz'


def test_empty_value():
    config = envyconfig.load('fixtures/basic.yaml')
    assert config['baz'] == ''
