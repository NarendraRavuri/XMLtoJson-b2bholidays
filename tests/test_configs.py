from src.configs import (
    var_ocg,
    CONVERSION_RATES,
    HOTEL_PRICE_CURRENCY,
    DEFAULT_NET_PRICE,
    DEFAULT_MARKUP,
    VALID_LANGUAGES,
    DEFAULT_LANGUAGE,
    DEFAULT_OPTIONS_QUOTA,
    MAX_OPTIONS_QUOTA,
    ALLOWED_CURRENCIES,
    DEFAULT_CURRENCY,
    ALLOWED_MARKET_VALUES,
    DEFAULT_MARKET,
    ALLOWED_NATIONALITIES,
    DEFAULT_NATIONALITY,
)

def test_var_ocg():
    assert var_ocg == "my_secret_handshake"

def test_conversion_rates():
    expected_rates = {
        ("USD", "EUR"): 0.9,
        ("USD", "GBP"): 0.77,
        ("EUR", "USD"): 1.1,
        ("EUR", "GBP"): 0.85,
        ("GBP", "USD"): 1.3,
        ("GBP", "EUR"): 1.17,
    }
    assert CONVERSION_RATES == expected_rates

def test_hotel_price_constants():
    assert HOTEL_PRICE_CURRENCY == "USD"
    assert DEFAULT_NET_PRICE == 132.42
    assert DEFAULT_MARKUP == 3.2

def test_language_and_quota_constants():
    assert VALID_LANGUAGES == {'en', 'fr', 'de', 'es'}
    assert DEFAULT_LANGUAGE == 'en'
    assert DEFAULT_OPTIONS_QUOTA == 20
    assert MAX_OPTIONS_QUOTA == 50

def test_currency_and_market_constants():
    assert ALLOWED_CURRENCIES == {"EUR", "USD", "GBP"}
    assert DEFAULT_CURRENCY == "EUR"
    assert ALLOWED_NATIONALITIES == {'US', 'GB', 'CA'}
    assert DEFAULT_NATIONALITY == 'US'
    assert ALLOWED_MARKET_VALUES == {'US', 'GB', 'CA', 'ES'}
    assert DEFAULT_MARKET == 'ES'
