import pytest
from requests import RequestException
from init import download_nltk_data
from app import app, search_hotels


@pytest.fixture
def client():
    with app.test_client() as client:
        return client


@pytest.fixture(scope='session')
def install_packages():
    download_nltk_data()


def test_get_api_endpoint(client):
    response = client.get('/I%20want%20to%20book%20a%20hotel%20in%20Spain')
    json_response = response.get_json()
    assert len(json_response) == 3
    assert response.status_code == 200


def test_post_api_endpoint(client):
    response = client.post('/I%20want%20to%20book%20a%20hotel%20in%20Spain')
    assert response.status_code == 405
    assert b"Method Not Allowed" in response.data


def test_get_hotel_returns_hotels_when_city_is_found_in_prompt(client):
    response = client.get('/I%20want%20to%20book%20a%20hotel%20in%20Spain')
    json_response = response.get_json()
    assert len(json_response) == 3
    assert response.status_code == 200


def test_get_hotel_returns_error_when_no_city_is_found_in_prompt(client):
    response = client.get('/I%20want%20to%20book%20a%20hotel')
    json_response = response.get_json()
    assert json_response == {"error": "No hotels found."}
    assert response.status_code == 200


def test_search_hotels_returns_hotels_when_city_found():
    result = search_hotels('I want to book a hotel in Spain')
    assert len(result) == 3


def test_search_hotels_returns_empty_when_no_city_found():
    result = search_hotels('I want to book a hotel')
    assert result is None


def mock_get(*args, **kwargs):
    raise RequestException


def test_request_exception(monkeypatch):
    monkeypatch.setattr("requests.get", mock_get)
    result = search_hotels("Amsterdam")
    assert result == 'An error occurred: '
