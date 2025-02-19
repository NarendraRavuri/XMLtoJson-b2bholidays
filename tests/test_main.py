import json
import datetime
import pytest
from src.main import process_request

def create_full_xml(
    start_date: datetime.date,
    end_date: datetime.date,
    options_quota: str = "20",
    language: str = "en",
    search_type: str = "Multiple",
    currency: str = "USD",
    nationality: str = "US",
    include_required_params: bool = True,
    destinations: str = ""
) -> str:
    if include_required_params:
        required_params = (
            '<Configuration>'
            '<Parameters>'
            '<Parameter password="pass" username="user" CompanyID="123456"/>'
            '</Parameters>'
            '</Configuration>'
        )
    else:
        required_params = (
            '<Configuration>'
            '<Parameters></Parameters>'
            '</Configuration>'
        )
    return f"""
    <AvailRQ xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
             xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <timeoutMilliseconds>25000</timeoutMilliseconds>
        <source>
            <languageCode>{language}</languageCode>
        </source>
        <optionsQuota>{options_quota}</optionsQuota>
        {required_params}
        <SearchType>{search_type}</SearchType>
        {destinations}
        <StartDate>{start_date.strftime('%d/%m/%Y')}</StartDate>
        <EndDate>{end_date.strftime('%d/%m/%Y')}</EndDate>
        <Currency>{currency}</Currency>
        <Nationality>{nationality}</Nationality>
    </AvailRQ>
    """

def test_process_request_valid():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=3)
    end = start + datetime.timedelta(days=3)
    xml_str = create_full_xml(start, end)
    result = process_request(xml_str)
    data = json.loads(result)
    assert isinstance(data, list)
    assert "id" in data[0]

def test_process_request_invalid_xml():
    result = process_request("not xml")
    data = json.loads(result)
    assert "error" in data
    assert data["error"] == "Invalid XML format."

def test_process_request_missing_required():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=3)
    end = start + datetime.timedelta(days=3)
    xml_str = create_full_xml(start, end, include_required_params=False)
    result = process_request(xml_str)
    data = json.loads(result)
    assert "error" in data
    assert "Missing" in data["error"]

def test_process_request_options_quota_too_high():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=3)
    end = start + datetime.timedelta(days=3)
    xml_str = create_full_xml(start, end, options_quota="60")
    result = process_request(xml_str)
    data = json.loads(result)
    assert "error" in data
    assert "optionsQuota cannot be greater than 50." in data["error"]

def test_process_request_start_date_too_soon():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=1)
    end = start + datetime.timedelta(days=3)
    xml_str = create_full_xml(start, end)
    result = process_request(xml_str)
    data = json.loads(result)
    assert "error" in data
    assert "StartDate must be at least 2 days after today." in data["error"]

def test_process_request_duration_too_short():
    today = datetime.date.today()
    start = today + datetime.timedelta(days=3)
    end = start + datetime.timedelta(days=2)
    xml_str = create_full_xml(start, end)
    result = process_request(xml_str)
    data = json.loads(result)
    assert "error" in data
    assert "The stay duration must be at least 3 nights." in data["error"]

def test_process_request_secret_handshake_failure(monkeypatch):
    today = datetime.date.today()
    start = today + datetime.timedelta(days=3)
    end = start + datetime.timedelta(days=3)
    xml_str = create_full_xml(start, end)
    from src import main
    monkeypatch.setattr(main, "var_ocg", "wrong_handshake")
    result = main.process_request(xml_str)
    data = json.loads(result)
    assert "error" in data
    assert "Secret handshake verification failed." in data["error"]
