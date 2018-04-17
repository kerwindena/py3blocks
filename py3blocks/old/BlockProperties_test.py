from .BlockProperties import BlockProperties


class Config_Mock:
    def __init__(self, d):
        self.__d = d

    def get(self, ign, v, fallback):
        return self.__d.get(v, fallback)


def test_creation():
    test_name = 'test-name'
    prop = BlockProperties(test_name)
    assert prop['name'] == test_name


def test_nop_change():
    prop = BlockProperties('foo')
    assert prop.read(Config_Mock({'align': None})) is False
    assert prop['align'] is None


def test_align_change():
    prop = BlockProperties('foo')
    align_value = 'align-value test'
    assert prop.read(Config_Mock({'align': align_value})) is True
    assert prop['align'] == align_value


def test_command_change():
    prop = BlockProperties('foo')
    command_value = 'command-value test'
    assert prop.read(Config_Mock({'command': command_value})) is True
    assert prop['_command'] == command_value
