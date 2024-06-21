import pytest
import requests_mock
from requests import RequestException
from init import download_nltk_data
from app import search_hotels


def setup_locations_return_data():
    locations_json = [
        {"dest_id": "123", "dest_type": "city"}
    ]

    return locations_json


def setup_hotel_return_data():
    search_json = {
        "result": [
            {"hotel_name": "Hotel1", "address": "Address1", "review_score_word": "Good", "min_total_price": "100",
             "url": "url1", "main_photo_url": "url1"},
            {"hotel_name": "Hotel1", "address": "Address1", "review_score_word": "Good", "min_total_price": "100",
             "url": "url1", "main_photo_url": "url1"},
            {"hotel_name": "Hotel1", "address": "Address1", "review_score_word": "Good", "min_total_price": "100",
             "url": "url1", "main_photo_url": "url1"}
        ]
    }

    return search_json


def mock_api_responses(mock_requests, locations_json, search_json):
    mock_requests.get('https://booking-com.p.rapidapi.com/v1/hotels/locations', json=locations_json)
    mock_requests.get('https://booking-com.p.rapidapi.com/v1/hotels/search', json=search_json)


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture(scope="session")
def install_packages():
    download_nltk_data()


def test_get_api_endpoint(mock_requests):
    mock_api_responses(mock_requests, setup_locations_return_data(), setup_hotel_return_data())
    result = search_hotels('I want to book a hotel in Spain')
    assert len(result) == 3


def test_search_hotels_returns_hotels_when_city_found(mock_requests):
    mock_api_responses(mock_requests, setup_locations_return_data(), setup_hotel_return_data())
    result = search_hotels('I want to book a hotel in Spain')
    assert len(result) == 3


def test_search_hotels_returns_empty_when_no_city_found(mock_requests):
    mock_api_responses(mock_requests, setup_locations_return_data(), setup_hotel_return_data())
    result = search_hotels('I want to book a hotel')
    assert result is None
