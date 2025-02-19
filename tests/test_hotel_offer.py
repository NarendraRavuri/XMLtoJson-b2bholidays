from src.hotel_offer import simulate_hotel_offer

def test_simulate_hotel_offer():
    offer = simulate_hotel_offer("EUR", "US")
    # Check that the offer has the expected structure
    assert isinstance(offer, dict)
    assert "id" in offer
    assert "hotelCodeSupplier" in offer
    assert "market" in offer
    assert "price" in offer
    price = offer["price"]
    for key in ["minimumSellingPrice", "currency", "net", "selling_price", "selling_currency", "markup", "exchange_rate"]:
        assert key in price
