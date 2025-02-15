from pwsproto.pws_request import (
    _pws_to_measurement_dict,
    url_param_to_status_dict,
    Measurement,
)
import logging


def test_measurement():
    sample_measurement = Measurement(42.0, "°C")
    assert sample_measurement.value == 42.0
    assert sample_measurement.unit == "°C"


def test_pws_to_measurement_dict():
    sample_measurements = _pws_to_measurement_dict(
        {
            "tempf": "42.0",
        }
    )
    assert len(sample_measurements) == 1
    expected_name = url_param_to_status_dict["tempf"].sensor_name
    assert sample_measurements[expected_name].value == 42.0


def test_pws_to_measurement_dict_unknown(caplog):
    with caplog.at_level(logging.WARNING):
        sample_measurements = _pws_to_measurement_dict(
            {
                "nonxist": "42.0",
            }
        )
        assert len(sample_measurements) == 0
        assert "Unknown parameter: nonxist" in caplog.text
