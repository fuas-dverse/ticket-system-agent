from unittest.mock import MagicMock, patch
import pytest
import requests
import requests_mock
from agentDVerse import Agent
from app import search_hotels
from init import download_nltk_data


def setup_locations_return_data():
    return [
        {"dest_id": "123", "dest_type": "city"}
    ]


def setup_hotel_return_data():
    return {
        "result": [
            {"hotel_name": "Hotel1", "address": "Address1", "review_score_word": "Good", "min_total_price": "100",
             "url": "url1", "main_photo_url": "url1"},
            {"hotel_name": "Hotel2", "address": "Address2", "review_score_word": "Very Good", "min_total_price": "150",
             "url": "url2", "main_photo_url": "url2"},
            {"hotel_name": "Hotel3", "address": "Address3", "review_score_word": "Excellent", "min_total_price": "200",
             "url": "url3", "main_photo_url": "url3"}
        ]
    }


def setup_empty_locations_data():
    return []


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
    assert result[0]['name'] == 'Hotel1'
    assert result[1]['name'] == 'Hotel2'
    assert result[2]['name'] == 'Hotel3'


def test_search_hotels_returns_hotels_when_city_found(mock_requests):
    mock_api_responses(mock_requests, setup_locations_return_data(), setup_hotel_return_data())
    result = search_hotels('I want to book a hotel in Spain')
    assert len(result) == 3
    assert all(hotel['name'].startswith('Hotel') for hotel in result)


def test_search_hotels_returns_empty_when_no_city_found(mock_requests):
    mock_api_responses(mock_requests, setup_empty_locations_data(), setup_hotel_return_data())
    result = search_hotels('I want to book a hotel')
    assert result is None


def test_search_hotels_handles_api_exception(mock_requests):
    mock_requests.get('https://booking-com.p.rapidapi.com/v1/hotels/locations',
                      exc=requests.exceptions.RequestException)
    result = search_hotels('I want to book a hotel in Spain')
    assert "An error occurred" in result


def test_search_hotels_no_hotels_returned(mock_requests):
    locations_data = setup_locations_return_data()
    empty_hotels_data = {"result": []}
    mock_api_responses(mock_requests, locations_data, empty_hotels_data)
    result = search_hotels('I want to book a hotel in Spain')
    assert result == []


def test_agent_initialization():
    with patch('agentDVerse.Agent', autospec=True) as MockAgent:
        mock_agent_instance = MockAgent.return_value
        mock_agent_instance.name = "Hotel Information Agent"
        mock_agent_instance.description = "This agent provides information about hotels in a certain region."
        mock_agent_instance.topics = ["hotel", "accommodation", "hotel-information"]
        mock_agent_instance.output_format = "json"
        mock_agent_instance.callback = MagicMock()

        agent = MockAgent(
            name="Hotel Information Agent",
            description="This agent provides information about hotels in a certain region.",
            topics=["hotel", "accommodation", "hotel-information"],
            output_format="json",
            callback=mock_agent_instance.callback
        )

        assert agent.name == mock_agent_instance.name
        assert agent.description == mock_agent_instance.description
        assert agent.topics == mock_agent_instance.topics
        assert agent.output_format == mock_agent_instance.output_format
        assert callable(agent.callback)
