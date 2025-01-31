import pytest
from unittest.mock import patch, MagicMock
from src.etl import request_to_api, extract, transform, load, connect_to_db

@pytest.fixture
def api_response():
    return {
        "data": [
            {
                "name": "Bitcoin",
                "symbol": "BTC",
                "max_supply": 21000000,
                "circulating_supply": 18500000,
                "quote": {
                    "GBP": {
                        "price": 30000,
                        "market_cap": 555000000000,
                        "market_cap_dominance": 60,
                        "percent_change_24h": 2.5,
                        "percent_change_30d": 10.0
                    }
                }
            }
        ]
    }

@pytest.fixture
def extracted_data():
    return [
        {
            "name": "Bitcoin",
            "symbol": "BTC",
            "max_supply": 21000000,
            "circulating_supply": 18500000,
            "price": 30000,
            "market_cap": 555000000000,
            "market_cap_dominance": 60,
            "percentage_change_24h": 2.5,
            "percentage_change_30d": 10.0
        }
    ]

@pytest.fixture
def transformed_data():
    return [
        {
            "name": "Bitcoin",
            "symbol": "BTC",
            "max_supply": "21000000",
            "circulating_supply": 18500000.00,
            "price": 30000.00,
            "market_cap": 555000000000.00,
            "market_cap_dominance": 60.00,
            "percentage_change_24h": 2.50,
            "percentage_change_30d": 10.00
        }
    ]

@patch('src.etl.requests.get')
def test_request_to_api(mock_get, api_response):
    mock_get.return_value.json.return_value = api_response
    data = request_to_api()
    assert data == api_response

def test_extract(api_response, extracted_data):
    data = extract(api_response)
    assert data == extracted_data

def test_transform(extracted_data, transformed_data):
    data = transform(extracted_data)
    assert data == transformed_data

@patch('src.etl.psycopg2.connect')
def test_load(mock_connect, transformed_data):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    result = load(transformed_data)
    assert result == "Crypto data inserted successfully!"
    mock_conn.cursor().execute.assert_called()
    mock_conn.commit.assert_called()
    mock_conn.close.assert_called()

@patch('src.etl.psycopg2.connect')
def test_connect_to_db(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    conn = connect_to_db()
    assert conn == mock_conn