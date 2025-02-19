from typing import Any, Dict
from .currency import convert_currency
from .configs import HOTEL_PRICE_CURRENCY, DEFAULT_NET_PRICE, DEFAULT_MARKUP


def simulate_hotel_offer(request_currency: str, market: str) -> Dict[str, Any]:
    """
    Simulates processing a hotel offer by applying markup and currency conversion.
    Returns a dictionary representing the hotel offer.
    """
    net_price = DEFAULT_NET_PRICE
    markup = DEFAULT_MARKUP
    base_selling_price = net_price * (1 + markup / 100)

    selling_price, exchange_rate = convert_currency(HOTEL_PRICE_CURRENCY, request_currency, base_selling_price)
    selling_currency = request_currency if HOTEL_PRICE_CURRENCY != request_currency else HOTEL_PRICE_CURRENCY

    offer = {
        "id": "A#1",
        "hotelCodeSupplier": "39971881",
        "market": market,
        "price": {
            "minimumSellingPrice": None,
            "currency": HOTEL_PRICE_CURRENCY,
            "net": net_price,
            "selling_price": round(selling_price, 2),
            "selling_currency": selling_currency,
            "markup": markup,
            "exchange_rate": exchange_rate
        }
    }
    return offer
