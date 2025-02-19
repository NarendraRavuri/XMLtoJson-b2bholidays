import xml.etree.ElementTree as ET
import datetime
from typing import Tuple


def parse_xml(xml_str: str) -> ET.Element:
    """
    Parses an XML string and returns the root element.
    Raises ET.ParseError if the XML is invalid.
    """
    return ET.fromstring(xml_str)


def extract_timeout(root: ET.Element) -> int:
    """
    Extracts the timeoutMilliseconds element from the XML, if available.
    Returns 0 if not found.
    """
    timeout_elem = root.find('timeoutMilliseconds')
    if timeout_elem is not None and timeout_elem.text and timeout_elem.text.isdigit():
        return int(timeout_elem.text)
    return 0


def parse_date(date_str: str) -> datetime.date:
    """
    Parses a date string in dd/mm/yyyy format.
    Raises ValueError if the format is incorrect.
    """
    return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()


def validate_dates(root: ET.Element) -> Tuple[datetime.date, datetime.date]:
    """
    Extracts and validates StartDate and EndDate.
    Ensures StartDate is at least 2 days after today and the stay is at least 3 nights.
    Raises ValueError if any condition is not met.
    """
    start_date_elem = root.find('StartDate')
    end_date_elem = root.find('EndDate')

    if start_date_elem is None or end_date_elem is None:
        raise ValueError("Missing StartDate or EndDate.")

    try:
        start_date = parse_date(start_date_elem.text.strip())
        end_date = parse_date(end_date_elem.text.strip())
    except ValueError:
        raise ValueError("Dates must be in dd/mm/yyyy format.")

    today = datetime.date.today()
    if (start_date - today).days < 2:
        raise ValueError("StartDate must be at least 2 days after today.")
    if (end_date - start_date).days < 3:
        raise ValueError("The stay duration must be at least 3 nights.")

    return start_date, end_date
