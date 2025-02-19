import xml.etree.ElementTree as ET
from typing import Any, Dict
from .configs import (
    VALID_LANGUAGES,
    DEFAULT_LANGUAGE,
    DEFAULT_OPTIONS_QUOTA,
    MAX_OPTIONS_QUOTA,
    ALLOWED_CURRENCIES,
    DEFAULT_CURRENCY,
    ALLOWED_NATIONALITIES,
    DEFAULT_NATIONALITY,
    ALLOWED_MARKET_VALUES,
    DEFAULT_MARKET,
    ALLOWED_ROOM_COUNT,
    ALLOWED_ROOM_GUEST_COUNT,
    ALLOWED_CHILD_COUNT_PER_ROOM
)


def validate_language_code(root: ET.Element) -> str:
    """
    Validates the language code from <source>/<languageCode>.
    Returns the language if valid, otherwise returns the default language.
    """
    language_elem = root.find('source/languageCode')
    language_code = language_elem.text.strip() if language_elem is not None and language_elem.text else DEFAULT_LANGUAGE
    # using `var_filters_cg` for language validation
    var_filters_cg = language_code not in VALID_LANGUAGES
    if var_filters_cg:
        return DEFAULT_LANGUAGE
    return language_code


def validate_options_quota(root: ET.Element) -> int:
    """
    Validates and returns the optionsQuota from the XML.
    Defaults to DEFAULT_OPTIONS_QUOTA if not provided.
    Raises ValueError if optionsQuota is above MAX_OPTIONS_QUOTA.
    """
    options_quota_elem = root.find('optionsQuota')
    if options_quota_elem is not None and options_quota_elem.text and options_quota_elem.text.isdigit():
        quota = int(options_quota_elem.text)
        if quota > MAX_OPTIONS_QUOTA:
            raise ValueError("optionsQuota cannot be greater than 50.")
        return quota
    return DEFAULT_OPTIONS_QUOTA


def extract_required_parameters(root: ET.Element) -> Dict[str, Any]:
    """
    Extracts required parameters: password, username, and CompanyID.
    Raises ValueError if any required parameter is missing or invalid.
    """
    param_elem = root.find('Configuration/Parameters/Parameter')
    if param_elem is None:
        raise ValueError("Missing Configuration Parameters.")

    password = param_elem.get("password")
    username = param_elem.get("username")
    company_id_str = param_elem.get("CompanyID")

    if not (password and username and company_id_str):
        raise ValueError("Missing required parameters: password, username, or CompanyID.")

    try:
        company_id = int(company_id_str)
    except ValueError:
        raise ValueError("CompanyID must be an integer.")

    return {"password": password, "username": username, "CompanyID": company_id}


def validate_search_type(root: ET.Element) -> str:
    """
    Extracts and validates the SearchType.
    For 'Single' type, verifies that exactly one AvailDestination is provided.
    Raises ValueError on validation failure.
    """
    search_type_elem = root.find('SearchType')
    search_type = search_type_elem.text.strip() if search_type_elem is not None and search_type_elem.text else "Multiple"

    if search_type == "Single":
        avail_destinations = root.find('AvailDestinations')
        if avail_destinations is None or len(avail_destinations.findall('*')) != 1:
            raise ValueError("For Single search type, exactly one AvailDestination is required.")
    return search_type


def extract_currency(root: ET.Element) -> str:
    """
    Extracts and validates the Currency element.
    Returns a valid currency or the default.
    """
    currency_elem = root.find('Currency')
    request_currency = currency_elem.text.strip() if currency_elem is not None and currency_elem.text else DEFAULT_CURRENCY
    if request_currency not in ALLOWED_CURRENCIES:
        return DEFAULT_CURRENCY
    return request_currency


def extract_nationality_and_market(root: ET.Element) -> str:
    """
    Extracts the Nationality and determines the market.
    Returns the nationality if valid; otherwise, returns the default market.
    """
    nationality_elem = root.find('Nationality')
    nationality = nationality_elem.text.strip() if nationality_elem is not None and nationality_elem.text else DEFAULT_NATIONALITY
    market = nationality if nationality in ALLOWED_NATIONALITIES else DEFAULT_MARKET
    return market


def validate_rooms_and_passengers(root: ET.Element) -> None:
    """
    Validates room and passenger rules:
    - Each <Paxes> block represents a room. Total rooms must not exceed ALLOWED_ROOM_COUNT.
    - Each <Pax> block in a room represents a passenger. Total passengers in the room must not exceed ALLOWED_ROOM_GUEST_COUNT.
    - Passengers aged 5 or under are considered 'Child'; older ones are 'Adult'.
    - A room with children must have at least one adult.
    - Total children per room must not exceed ALLOWED_CHILD_COUNT_PER_ROOM.
    """
    rooms = root.findall('.//Paxes')
    if len(rooms) > ALLOWED_ROOM_COUNT:
        raise ValueError("Exceeded maximum allowed room count.")

    for room in rooms:
        # Find all <Pax> elements within this room
        pax_list = room.findall('.//Pax')
        if len(pax_list) > ALLOWED_ROOM_GUEST_COUNT:
            raise ValueError("Exceeded maximum allowed guests per room.")

        children_count = 0
        adult_count = 0
        for pax in pax_list:
            try:
                age = int(pax.get("age", "0"))
            except ValueError:
                raise ValueError("Invalid age value in Pax element.")

            if age <= 5:
                children_count += 1
            else:
                adult_count += 1

        if children_count > ALLOWED_CHILD_COUNT_PER_ROOM:
            raise ValueError("Exceeded maximum children per room.")
        if children_count > 0 and adult_count == 0:
            raise ValueError("Each room with children must have at least one adult.")
