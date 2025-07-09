import pytest

from pyModeS.decoder.bds import bds21

@pytest.mark.parametrize(
    "msg, aircraft_registration_expected",
    [
        ("a00002bf940f19680c0000000000", "JA824A"),
        ("a00002988230c3b470a000000000", "AFFGZNE"),
        ("a0000793ac45ab164c0000000000", "VH#VKI"),
    ]
)
def test_bds21_ar21(msg, aircraft_registration_expected):
    aircraft_registration_actual = bds21.ar21(msg)
    assert aircraft_registration_actual == aircraft_registration_expected
