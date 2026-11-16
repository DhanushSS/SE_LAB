"""Property-based tests for the train fare input parsers."""
import re
import pytest
from hypothesis import given, strategies as st, example
from train_fare import parse_pnr, journey_distance, berth_type, BERTHS

ascii_digits = st.text(alphabet='0123456789', min_size=10, max_size=10)

@given(ascii_digits)
def test_parse_pnr_valid(pnr):
    assert parse_pnr(pnr) == (int(pnr[0]), int(pnr[1:]))

@given(st.one_of(st.none(), st.integers(), st.text().filter(lambda s: re.fullmatch(r'[0-9]{10}', s) is None)))
@example('')
def test_parse_pnr_invalid(value):
    with pytest.raises(ValueError):
        parse_pnr(value)

@given(st.lists(st.integers(min_value=0, max_value=100000), min_size=2, max_size=12).map(sorted))
def test_journey_distance_valid(distances):
    assert journey_distance(','.join(map(str, distances))) == distances[-1] - distances[0]

@given(st.one_of(st.none(), st.integers(), st.sampled_from(['', '1', '1,,3', '-1,2', '10,5', '1,x'])))
def test_journey_distance_invalid(value):
    with pytest.raises(ValueError):
        journey_distance(value)

@given(st.sampled_from(['S', 'A', 'B']), st.integers(min_value=1, max_value=99), st.integers(min_value=1, max_value=72))
def test_berth_type_valid(prefix, coach_number, number):
    assert berth_type(f'{prefix.lower()}{coach_number}-{number}') == (f'{prefix}{coach_number}', BERTHS[number % 8])

@given(st.one_of(st.none(), st.integers(), st.sampled_from(['', 'S3-0', 'S3-73', '-1', 'S3-x', 'S3-1-2'])))
def test_berth_type_invalid(value):
    with pytest.raises(ValueError):
        berth_type(value)
