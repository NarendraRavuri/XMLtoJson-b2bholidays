from typing import Tuple
from .configs import CONVERSION_RATES


def convert_currency(from_currency: str, to_currency: str, price: float) -> Tuple[float, float]:
    """
    Converts the price from one currency to another using predefined conversion rates.
    Returns a tuple of (converted_price, exchange_rate).
    If no conversion rate is found, assumes a 1:1 conversion.
    """
    if from_currency == to_currency:
        return price, 1.0
    rate = CONVERSION_RATES.get((from_currency, to_currency), 1.0)
    return price * rate, rate
