import datetime
import pytest
import xml.etree.ElementTree as ET
from src.xml_parser import parse_xml, extract_timeout, parse_date, validate_dates


def test_parse_xml_valid():
    xml_str = "<root><child>value</child></root>"
    root = parse_xml(xml_str)
    assert root.tag == "root"

def test_parse_xml_invalid():
    with pytest.raises(ET.ParseError):
        parse_xml("not xml")

def test_extract_timeout_present():
    xml_str = "<root><timeoutMilliseconds>12345</timeoutMilliseconds></root>"
    root = parse_xml(xml_str)
    assert extract_timeout(root) == 12345

def test_extract_timeout_absent():
    xml_str = "<root></root>"
    root = parse_xml(xml_str)
    assert extract_timeout(root) == 0

def test_parse_date_valid():
    date = parse_date("01/01/2025")
    assert date == datetime.date(2025, 1, 1)

def test_parse_date_invalid():
    with pytest.raises(ValueError):
        parse_date("2025-01-01")

def create_dates_xml(start_date: datetime.date, end_date: datetime.date) -> str:
    return f"""
    <AvailRQ>
        <StartDate>{start_date.strftime('%d/%m/%Y')}</StartDate>
        <EndDate>{end_date.strftime('%d/%m/%Y')}</EndDate>
    </AvailRQ>
    """

def test_validate_dates_valid():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=3)
    end = start + datetime.timedelta(days=3)
    xml_str = create_dates_xml(start, end)
    root = parse_xml(xml_str)
    start_val, end_val = validate_dates(root)
    assert start_val == start
    assert end_val == end

def test_validate_dates_start_too_soon():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=1)  # Too soon
    end = start + datetime.timedelta(days=3)
    xml_str = create_dates_xml(start, end)
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="StartDate must be at least 2 days after today."):
        validate_dates(root)

def test_validate_dates_duration_too_short():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=3)
    end = start + datetime.timedelta(days=2)  # Too short
    xml_str = create_dates_xml(start, end)
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="The stay duration must be at least 3 nights."):
        validate_dates(root)

def test_validate_dates_invalid_format():
    # Provide invalid date formats (using dashes instead of slashes)
    xml_str = """
    <AvailRQ>
        <StartDate>14-10-2024</StartDate>
        <EndDate>16-10-2024</EndDate>
    </AvailRQ>
    """
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="Dates must be in dd/mm/yyyy format."):
        validate_dates(root)

def test_validate_dates_missing_elements():
    # Provide an XML that does not include StartDate and EndDate.
    xml_str = "<AvailRQ></AvailRQ>"
    root = parse_xml(xml_str)
    with pytest.raises(ValueError, match="Missing StartDate or EndDate."):
        validate_dates(root)
