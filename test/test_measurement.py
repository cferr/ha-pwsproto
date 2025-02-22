from pwsproto.pws_request import (
    pws_to_measurement_dict,
    url_param_to_status_dict,
    Measurement,
)


def test_measurement():
    sample_measurement = Measurement(42.0, "°C")
    assert sample_measurement.value == 42.0
    assert sample_measurement.unit == "°C"


def test_pws_to_measurement_dict():
    sample_measurements, unmatched_params = pws_to_measurement_dict(
        {
            "tempf": "42.0",
        }
    )
    assert len(sample_measurements) == 1
    assert len(unmatched_params) == 0
    expected_name = url_param_to_status_dict["tempf"].sensor_name
    assert sample_measurements[expected_name].value == 42.0


def test_pws_to_measurement_dict_unknown():
    sample_measurements, unmatched_params = pws_to_measurement_dict(
        {
            "nonxist": "42.0",
        }
    )
    assert len(sample_measurements) == 0
    assert len(unmatched_params) == 1
    assert "nonxist" in unmatched_params
