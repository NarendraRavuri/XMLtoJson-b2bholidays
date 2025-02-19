import xml.etree.ElementTree as ET
import pytest
from src.xml_parser import parse_xml
from src.validators import (
    validate_language_code,
    validate_options_quota,
    extract_required_parameters,
    validate_search_type,
    validate_rooms_and_passengers,
    extract_currency,
    extract_nationality_and_market,
    DEFAULT_LANGUAGE,
    DEFAULT_OPTIONS_QUOTA,
    VALID_LANGUAGES
)

def create_language_xml(lang: str) -> str:
    return f"""
    <AvailRQ>
        <source>
            <languageCode>{lang}</languageCode>
        </source>
    </AvailRQ>
    """

def test_validate_language_code_valid():
    xml_str = create_language_xml("en")
    root = parse_xml(xml_str)
    assert validate_language_code(root) == "en"

def test_validate_language_code_invalid():
    xml_str = create_language_xml("xx")
    root = parse_xml(xml_str)
    # Should fallback to DEFAULT_LANGUAGE since "xx" is not in VALID_LANGUAGES
    assert validate_language_code(root) == DEFAULT_LANGUAGE

def test_validate_language_code_missing():
    xml_str = "<AvailRQ><source></source></AvailRQ>"
    root = parse_xml(xml_str)
    assert validate_language_code(root) == DEFAULT_LANGUAGE

def create_options_quota_xml(quota: str) -> str:
    return f"""
    <AvailRQ>
        <optionsQuota>{quota}</optionsQuota>
    </AvailRQ>
    """

def test_validate_options_quota_valid():
    xml_str = create_options_quota_xml("30")
    root = parse_xml(xml_str)
    assert validate_options_quota(root) == 30

def test_validate_options_quota_missing():
    xml_str = "<AvailRQ></AvailRQ>"
    root = parse_xml(xml_str)
    assert validate_options_quota(root) == DEFAULT_OPTIONS_QUOTA

def test_validate_options_quota_too_high():
    xml_str = create_options_quota_xml("60")
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="optionsQuota cannot be greater than 50."):
        validate_options_quota(root)

def create_required_parameters_xml(password="pass", username="user", company_id="123456") -> str:
    return f"""
    <AvailRQ>
        <Configuration>
            <Parameters>
                <Parameter password="{password}" username="{username}" CompanyID="{company_id}"/>
            </Parameters>
        </Configuration>
    </AvailRQ>
    """

def test_extract_required_parameters_valid():
    xml_str = create_required_parameters_xml("pass", "user", "123456")
    root = parse_xml(xml_str)
    params = extract_required_parameters(root)
    assert params["password"] == "pass"
    assert params["username"] == "user"
    assert params["CompanyID"] == 123456

def test_extract_required_parameters_missing():
    xml_str = """
    <AvailRQ>
        <Configuration>
            <Parameters>
                <Parameter username="user" CompanyID="123456"/>
            </Parameters>
        </Configuration>
    </AvailRQ>
    """
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="Missing required parameters"):
        extract_required_parameters(root)

def test_extract_required_parameters_invalid_companyid():
    xml_str = create_required_parameters_xml("pass", "user", "notanumber")
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="CompanyID must be an integer."):
        extract_required_parameters(root)

def create_search_type_xml(search_type: str, destinations: str = "") -> str:
    return f"""
    <AvailRQ>
        <SearchType>{search_type}</SearchType>
        {destinations}
    </AvailRQ>
    """

def test_validate_search_type_multiple():
    xml_str = create_search_type_xml("Multiple")
    root = parse_xml(xml_str)
    assert validate_search_type(root) == "Multiple"

def test_validate_search_type_single_valid():
    destinations_xml = "<AvailDestinations><Destination>Dest1</Destination></AvailDestinations>"
    xml_str = create_search_type_xml("Single", destinations_xml)
    root = parse_xml(xml_str)
    assert validate_search_type(root) == "Single"

def test_validate_search_type_single_invalid():
    # No destinations provided
    xml_str = create_search_type_xml("Single")
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="For Single search type, exactly one AvailDestination is required."):
        validate_search_type(root)

    # More than one destination provided
    destinations_xml = """
    <AvailDestinations>
        <Destination>Dest1</Destination>
        <Destination>Dest2</Destination>
    </AvailDestinations>
    """
    xml_str = create_search_type_xml("Single", destinations_xml)
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="For Single search type, exactly one AvailDestination is required."):
        validate_search_type(root)

def create_currency_xml(currency: str) -> str:
    return f"""
    <AvailRQ>
        <Currency>{currency}</Currency>
    </AvailRQ>
    """

def test_extract_currency_valid():
    xml_str = create_currency_xml("USD")
    root = parse_xml(xml_str)
    assert extract_currency(root) == "USD"

def test_extract_currency_invalid():
    xml_str = create_currency_xml("ABC")
    root = parse_xml(xml_str)
    assert extract_currency(root) == "EUR"  # default fallback

def test_extract_currency_missing():
    xml_str = "<AvailRQ></AvailRQ>"
    root = parse_xml(xml_str)
    assert extract_currency(root) == "EUR"

def create_nationality_xml(nationality: str) -> str:
    return f"""
    <AvailRQ>
        <Nationality>{nationality}</Nationality>
    </AvailRQ>
    """

def test_extract_nationality_and_market_valid():
    xml_str = create_nationality_xml("US")
    root = parse_xml(xml_str)
    assert extract_nationality_and_market(root) == "US"

def test_extract_nationality_and_market_invalid():
    xml_str = create_nationality_xml("XX")
    root = parse_xml(xml_str)
    assert extract_nationality_and_market(root) == "ES"  # default market

def test_extract_nationality_and_market_missing():
    xml_str = "<AvailRQ></AvailRQ>"
    root = parse_xml(xml_str)
    # Assumes default nationality "US" if missing
    assert extract_nationality_and_market(root) == "US"

def create_xml_with_rooms(rooms_xml: str) -> ET.Element:
    """
    Helper function to wrap provided room XML into a valid root.
    """
    xml_str = f"<AvailRQ>{rooms_xml}</AvailRQ>"
    return ET.fromstring(xml_str)

def test_valid_room_and_passengers():
    # Valid scenario: one room with 1 child and 2 adults.
    xml_str = """
    <Paxes>
        <Pax age="4"/>
        <Pax age="30"/>
        <Pax age="25"/>
    </Paxes>
    """
    root = create_xml_with_rooms(xml_str)
    # This should pass without raising an error.
    validate_rooms_and_passengers(root)

def test_exceed_max_rooms():
    # Exceed allowed room count.
    # Suppose ALLOWED_ROOM_COUNT is 5; we create 6 <Paxes> blocks.
    rooms = "".join(["<Paxes><Pax age='30'/></Paxes>" for _ in range(6)])
    root = create_xml_with_rooms(rooms)
    with pytest.raises(ValueError, match="Exceeded maximum allowed room count."):
        validate_rooms_and_passengers(root)

def test_exceed_max_guests_per_room():
    # Create one room with 5 passengers (ALLOWED_ROOM_GUEST_COUNT is 4).
    xml_str = """
    <Paxes>
        <Pax age="30"/>
        <Pax age="25"/>
        <Pax age="40"/>
        <Pax age="35"/>
        <Pax age="28"/>
    </Paxes>
    """
    root = create_xml_with_rooms(xml_str)
    with pytest.raises(ValueError, match="Exceeded maximum allowed guests per room."):
        validate_rooms_and_passengers(root)

def test_exceed_max_children_per_room():
    # Create one room with 3 children and 1 adult (ALLOWED_CHILD_COUNT_PER_ROOM is 2).
    xml_str = """
    <Paxes>
        <Pax age="4"/>
        <Pax age="3"/>
        <Pax age="2"/>
        <Pax age="30"/>
    </Paxes>
    """
    root = create_xml_with_rooms(xml_str)
    with pytest.raises(ValueError, match="Exceeded maximum children per room."):
        validate_rooms_and_passengers(root)

def test_room_with_children_but_no_adult():
    # Create one room with children only.
    xml_str = """
    <Paxes>
        <Pax age="4"/>
        <Pax age="3"/>
    </Paxes>
    """
    root = create_xml_with_rooms(xml_str)
    with pytest.raises(ValueError, match="Each room with children must have at least one adult."):
        validate_rooms_and_passengers(root)

def test_invalid_age_value():
    # Create a room with one Pax element having an invalid age attribute.
    xml_str = """
    <Paxes>
        <Pax age="invalid"/>
        <Pax age="30"/>
    </Paxes>
    """
    root = create_xml_with_rooms(xml_str)
    with pytest.raises(ValueError, match="Invalid age value in Pax element."):
        validate_rooms_and_passengers(root)

