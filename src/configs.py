from typing import Tuple, Dict

# __define_ocg__
var_ocg = "my_secret_handshake"  # Secret handshake variable

CONVERSION_RATES: Dict[Tuple[str, str], float] = {
    ("USD", "EUR"): 0.9,
    ("USD", "GBP"): 0.77,
    ("EUR", "USD"): 1.1,
    ("EUR", "GBP"): 0.85,
    ("GBP", "USD"): 1.3,
    ("GBP", "EUR"): 1.17,
}


# Pricing simulation constants
HOTEL_PRICE_CURRENCY = "USD"
DEFAULT_NET_PRICE = 132.42
DEFAULT_MARKUP = 3.2

# Constants for Languages
VALID_LANGUAGES = {"en", "fr", "de", "es"}
DEFAULT_LANGUAGE = "en"

# Constants for Options Quota
DEFAULT_OPTIONS_QUOTA = 20
MAX_OPTIONS_QUOTA = 50

# Constants for Nationality
ALLOWED_NATIONALITIES = {"US", "GB", "CA"}
DEFAULT_NATIONALITY = "US"

# Constants for currency
ALLOWED_CURRENCIES = {"EUR", "USD", "GBP"}
DEFAULT_CURRENCY = "EUR"

# Constants for market
ALLOWED_MARKET_VALUES = {"US", "GB", "CA", "ES"}
DEFAULT_MARKET = "ES"

# Room and Passenger Rules configuration
ALLOWED_ROOM_COUNT = 5             # Maximum allowed rooms
ALLOWED_ROOM_GUEST_COUNT = 4       # Maximum guests per room
ALLOWED_CHILD_COUNT_PER_ROOM = 2   # Maximum children allowed per room