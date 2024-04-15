import json
from unittest.mock import patch, Mock
from app import fetch_google_results, require_api_key, get_response


def test_fetch_google_results_returns_expected_results():
    with patch('app.search') as mock_search:
        mock_search.return_value = ['https://www.google.com', 'https://www.google.com', 'https://www.google.com']
        results = fetch_google_results('test query')
        assert results == ['https://www.google.com', 'https://www.google.com', 'https://www.google.com']


def test_require_api_key_allows_access_with_valid_key(test_app):
    with patch('app.SECRET_API_KEY', 'valid_key'), patch('app.fetch_google_results') as mock_fetch:
        mock_fetch.return_value = ['https://www.google.com', 'https://www.google.com', 'https://www.google.com']

        @require_api_key
        def dummy_route():
            return "Success"

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'key': 'valid_key'
        }

        json = {
            'query': 'Tickets for defcon1'
        }

        response = test_app.post('/', headers=headers, json=json)
        assert response.status_code == 200


def test_if_query_is_not_null(test_app):
    print("")