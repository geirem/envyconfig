import envyconfig


def test_use_default_when_env_var_is_not_defined():
    config = envyconfig.load('fixtures/basic_env.yaml')
    assert config['foo'] == 'bar'


def test_with_env_var(monkeypatch):
    expected = 'some string'
    monkeypatch.setenv("TESTENVVAR", expected)
    config = envyconfig.load('fixtures/basic_env.yaml')
    assert config['foo'] == expected
