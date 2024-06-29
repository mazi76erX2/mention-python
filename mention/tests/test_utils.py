import pytest
from typing import Literal
import utils

def test_transform_date():
    result = utils.transform_date('2018-11-25 12:00')
    assert result == '2018-11-25T12%3A00%3A00.12345%2B00%3A00'

@pytest.mark.parametrize("input_value, expected", [
    (True, '1'),
    (False, '0')
])
def test_transform_boolean(input_value: bool, expected: str):
    result = utils.transform_boolean(input_value)
    assert result == expected

@pytest.mark.parametrize("input_tone, expected", [
    ('negative', '-1'),
    ('neutral', '0'),
    ('positive', '1')
])
def test_transform_tone(input_tone: Literal['negative', 'neutral', 'positive'], expected: str):
    result = utils.transform_tone(input_tone)
    assert result == expected