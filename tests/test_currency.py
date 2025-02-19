import pytest
from src.currency import convert_currency

def test_convert_currency_same():
    price, rate = convert_currency("USD", "USD", 100)
    assert price == 100
    assert rate == 1.0

def test_convert_currency_valid():
    price, rate = convert_currency("USD", "EUR", 100)
    assert rate == 0.9
    assert price == 100 * 0.9

def test_convert_currency_fallback():
    # For a conversion pair not defined, fallback to 1:1
    price, rate = convert_currency("ABC", "DEF", 100)
    assert price == 100
    assert rate == 1.0
