"""Line coverage tests for the unchanged train_fare application.

Run from this directory:
    coverage run --source=train_fare -m pytest CodeCoverageTest_PES2UG24CS154_application.py
    coverage report -m
"""

import pytest

from train_fare import base_fare, concession, tatkal_charge


@pytest.mark.parametrize("travel_class,distance,expected", [
    ("SL", 500, 500), ("3A", 100, 200),
    ("2A", 100, 300), ("1A", 100, 500), ("SL", 10, 50),
])
def test_base_fare(travel_class, distance, expected):
    assert base_fare(travel_class, distance) == expected


@pytest.mark.parametrize("travel_class,distance,message", [
    ("INVALID", 100, "unknown class"), ("SL", 0, "invalid distance"),
])
def test_invalid_base_fare(travel_class, distance, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        base_fare(travel_class, distance)


@pytest.mark.parametrize("age,gender,tatkal,expected", [
    (30, "M", True, 0), (4, "F", False, 100),
    (12, "M", False, 50), (60, "F", False, 50),
    (60, "M", False, 40), (30, "M", False, 0),
])
def test_concessions(age, gender, tatkal, expected):
    assert concession(age, gender, tatkal) == expected


@pytest.mark.parametrize("travel_class,fare,expected", [
    ("SL", 2000, 200), ("3A", 1000, 300),
    ("SL", 5000, 400), ("SL", 500, 100),
])
def test_tatkal_charges(travel_class, fare, expected):
    assert tatkal_charge(travel_class, fare) == expected
