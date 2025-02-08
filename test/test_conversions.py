from pwsproto.station import str_to_float, str_to_int


def test_int_conversion():
    assert str_to_int("1") == 1


def test_float_conversion():
    assert str_to_float("1.0") == 1.0
