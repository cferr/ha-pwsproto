from pwsproto.station import UrlConversion, str_to_float, str_to_int


def test_int_conversion():
    converter = UrlConversion("test", str_to_int)
    assert converter("1") == 1


def test_float_conversion():
    converter = UrlConversion("test", str_to_float)
    assert converter("1.0") == 1.0
