import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from .configs import var_ocg
from .xml_parser import parse_xml, extract_timeout, validate_dates
from .validators import (
    validate_language_code,
    validate_options_quota,
    extract_required_parameters,
    validate_search_type,
    extract_currency,
    extract_nationality_and_market,
    validate_rooms_and_passengers
)
from .hotel_offer import simulate_hotel_offer


def process_request(xml_str: str) -> str:
    """
    Processes the XML request, validates all requirements, applies business logic,
    and returns a JSON response.
    """
    try:
        root = parse_xml(xml_str)
        # Extract optional timeout (not used in business logic here)
        _ = extract_timeout(root)

        # Validate and extract each required part
        language_code = validate_language_code(root)
        _ = validate_options_quota(root)
        _ = extract_required_parameters(root)
        _ = validate_search_type(root)
        start_date, end_date = validate_dates(root)
        request_currency = extract_currency(root)
        market = extract_nationality_and_market(root)

        # Validate room and passenger rules
        validate_rooms_and_passengers(root)

        # Simulate hotel offer processing
        offer = simulate_hotel_offer(request_currency, market)

        # Secret handshake check using var_ocg
        if var_ocg != "my_secret_handshake":
            raise ValueError("Secret handshake verification failed.")

        # Return a list of offers in JSON format
        response: List[Dict[str, Any]] = [offer]
        return json.dumps(response, indent=2)

    except ET.ParseError:
        return json.dumps({"error": "Invalid XML format."})
    except ValueError as e:
        return json.dumps({"error": str(e)})

# Example usage:
if __name__ == "__main__":
    sample_xml = """
    <AvailRQ xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
             xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <timeoutMilliseconds>25000</timeoutMilliseconds>
        <source>
            <languageCode>en</languageCode>
        </source>
        <optionsQuota>20</optionsQuota>
        <Configuration>
            <Parameters>
                <Parameter password="XXXXXXXXXX" username="YYYYYYYYY" CompanyID="123456"/>
            </Parameters>
        </Configuration>
        <SearchType>Multiple</SearchType>
        <StartDate>14/10/2025</StartDate>
        <EndDate>26/10/2025</EndDate>
        <Currency>USD</Currency>
        <Nationality>US</Nationality>
    </AvailRQ>
    """
    print(process_request(sample_xml))
