# XMLtoJson-b2bholidays

This is a Python project that processes XML requests for hotel offers, validates them against specific business rules, and returns a JSON response. It simulates a real-world scenario by converting an XML request into a JSON output while performing various validations (such as language, quota, dates, currency conversion, etc.) and applying business logic. This project was developed as part of a coding assessment for a Senior Python Developer role at B2BHolidays.

## Features

- **XML Parsing**: Utilizes Python's built-in `xml.etree.ElementTree` for parsing XML requests.
- **Business Logic Validation**: Validates elements such as language code, options quota, required parameters, search type, dates, currency, and nationality.
- **Currency Conversion**: Applies conversion rates to simulate pricing across different currencies.
- **Hotel Offer Simulation**: Calculates hotel offer details, applying markup to the base price and converting currency if needed.
- **Centralized Configuration**: All configuration constants and secret variables are maintained in a dedicated configuration module (`src/config.py`).
- **Full Test Coverage**: Tested using `pytest` and `coverage` to ensure all branches and functions work as expected.

## Project Structure

```
XMLtoJson-b2bholidays/
├── problem_statement/
│   ├── mail_communication.txt                                 # Mail communication text to provide the context
│   └── SeniorPythonDeveloperCodingAssessment_v2.pdf           # PDF file with deatiled requirements with business logic
├── src/
│   ├── __init__.py
│   ├── config.py                                              # Configuration file with constants and secret variables
│   ├── currency.py                                            # Currency conversion logic
│   ├── hotel_offer.py                                         # Hotel offer simulation logic
│   ├── main.py                                                # Main entry point to process XML requests
│   ├── validators.py                                          # Business rule validators for the XML input
│   └── xml_parser.py                                          # XML parsing and date validation utilities
├── tests/
│   ├── __init__.py
│   ├── test_config.py                                         # Tests for configuration constants
│   ├── test_currency.py                                       # Tests for currency conversion logic
│   ├── test_hotel_offer.py                                    # Tests for hotel offer simulation
│   ├── test_main.py                                           # Tests for the main processing function
│   ├── test_validators.py                                     # Tests for validation functions
│   └── test_xml_parser.py                                     # Tests for XML parsing and date validation
├── README.md                                                  # This file
├── requirements.txt                                           # Project dependencies
└── Dockerfile                                                 # To containerize the application in future
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/NarendraRavuri/XMLtoJson-b2bholidays.git
   cd XMLtoJson-b2bholidays
   ```

2. **Create and Activate a Virtual Environment using conda**

   ```bash
   conda create -n b2bholidays python=3.11.0
   conda activate b2bholidays
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the main module:

```bash
python -m src.main
```

This command processes a hard-coded sample XML request in `src/main.py` and prints the JSON response.

## Running Tests

The project uses `pytest` for testing. To run all tests with detailed output, execute:

```bash
pytest -v
```

For a coverage report, first install `coverage`:

```bash
pip install coverage
```

Then run:

```bash
coverage run -m pytest
coverage report -m
```

To generate an interactive HTML report:

```bash
coverage html
```

Open the `htmlcov/index.html` file in your browser for detailed coverage information.

## Configuration

All configuration settings are defined in `src/config.py`. This file includes:

- **Secret Handshake**:  
  `var_ocg = "my_secret_handshake"` is used to verify the secret handshake in the business logic.

- **Currency Conversion Rates**:  
  `CONVERSION_RATES` defines the conversion rates between different currencies.

- **Pricing Simulation Constants**:  
  `HOTEL_PRICE_CURRENCY`, `DEFAULT_NET_PRICE`, and `DEFAULT_MARKUP` are used to simulate hotel pricing.

- **Validation Constants**:  
  `var_filters_cg`, `DEFAULT_LANGUAGE`, `DEFAULT_OPTIONS_QUOTA`, and `MAX_OPTIONS_QUOTA` are used for language and options quota validation.

- **Market and Currency Validation**:  
  `ALLOWED_CURRENCIES`, `DEFAULT_CURRENCY`, `ALLOWED_MARKET_VALUES`, and `DEFAULT_MARKET` ensure that only allowed values are processed.



## Contact

If you have any questions or issues, please open an issue in the repository or contact the project maintainer.

