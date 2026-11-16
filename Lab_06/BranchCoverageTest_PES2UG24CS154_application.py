"""Exercise every decision outcome and important fare boundaries.

Run from this directory:
    coverage run --branch --source=train_fare -m pytest BranchCoverageTest_PES2UG24CS154_application.py
    coverage report -m
"""

import pytest

from train_fare import base_fare, concession, tatkal_charge


@pytest.mark.parametrize("travel_class,distance,expected", [
    ("SL", 49, 50), ("SL", 50, 50), ("SL", 51, 51),
    ("3A", 24, 50), ("3A", 25, 50), ("3A", 26, 52),
    ("2A", 10, 50), ("2A", 100, 300),
    ("1A", 9, 50), ("1A", 10, 50), ("1A", 11, 55),
])
def test_minimum_fare_boundary(travel_class, distance, expected):
    assert base_fare(travel_class, distance) == expected


@pytest.mark.parametrize("travel_class,distance,message", [
    ("UNKNOWN", 100, "unknown class"),
    ("sl", 100, "unknown class"),
    ("UNKNOWN", 0, "unknown class"),
    ("SL", 0, "invalid distance"),
    ("3A", -1, "invalid distance"),
])
def test_rejected_fares(travel_class, distance, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        base_fare(travel_class, distance)


@pytest.mark.parametrize("age,gender,tatkal,expected", [
    (0, "F", False, 100), (4, "M", False, 100),
    (5, "F", False, 50), (12, "M", False, 50),
    (13, "F", False, 0), (59, "M", False, 0),
    (60, "F", False, 50), (60, "M", False, 40),
    (80, "F", False, 50), (80, "M", False, 40),
    (4, "F", True, 0), (12, "M", True, 0),
    (30, "M", True, 0), (60, "F", True, 0), (60, "M", True, 0),
])
def test_concession_decisions(age, gender, tatkal, expected):
    assert concession(age, gender, tatkal) == expected


@pytest.mark.parametrize("travel_class,fare,expected", [
    ("SL", 990, 100), ("SL", 1000, 100), ("SL", 1010, 101),
    ("SL", 3990, 399), ("SL", 4000, 400), ("SL", 4010, 400),
    ("3A", 330, 100), ("3A", 334, 100), ("3A", 337, 101),
    ("3A", 1330, 399), ("3A", 1334, 400), ("3A", 1337, 400),
    ("2A", 1000, 300), ("1A", 1000, 300),
    ("SL", 1009, 100), ("3A", 1009, 302),
])
def test_tatkal_rate_floor_and_cap(travel_class, fare, expected):
    assert tatkal_charge(travel_class, fare) == expected
