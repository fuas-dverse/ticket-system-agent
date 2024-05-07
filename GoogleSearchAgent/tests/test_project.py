from unittest.mock import patch
import pytest

from app import fetch_google_results, app


@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_fetch_google_results_returns_expected_results():
    with patch('app.search') as mock_search:
        mock_search.return_value = ['https://www.google.com', 'https://www.google.com', 'https://www.google.com']
        results = fetch_google_results('test query')
        assert results == ['https://www.google.com', 'https://www.google.com', 'https://www.google.com']


def test_require_api_key_allows_access_with_valid_key(test_app):
    with patch('os.getenv', return_value='valid_key'):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer valid_key'
        }
        response = test_app.post('/', headers=headers, json={'query': 'test query'})
        assert response.status_code == 200


def test_require_api_key_denies_access_with_invalid_key(test_app):
    with patch('os.getenv', return_value='valid_key'):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer invalid_key'
        }
        response = test_app.post('/', headers=headers, json={'query': 'test query'})
        assert response.status_code == 401


def test_fetch_google_results_handles_errors_gracefully():
    with patch('app.search') as mock_search:
        mock_search.side_effect = Exception("Network Error")
        results = fetch_google_results('test query')
        assert results == []


def test_get_response_returns_valid_results(test_app):
    with patch('app.fetch_google_results') as mock_fetch, \
            patch('os.getenv', return_value='valid_key'):
        mock_fetch.return_value = ['https://www.example.com']
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer valid_key'
        }
        response = test_app.post('/', headers=headers, json={'query': 'test query'})
        assert response.status_code == 200
        assert response.json == {'response': ['https://www.example.com']}


def test_get_response_with_empty_query(test_app):
    with patch('app.fetch_google_results') as mock_fetch, \
            patch('os.getenv', return_value='valid_key'):
        mock_fetch.return_value = ['https://www.example.com']
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer valid_key'
        }
        response = test_app.post('/', headers=headers, json={'query': ''})  # Empty query
        assert response.status_code == 400
        assert response.json == {'error': 'You must fill in a search query!'}


# Add a test to ensure that the security headers are correctly applied
# Trying to modify the security headers in a request should not affect the original security settings
def test_security_headers_are_applied(test_app):
    with patch('app.fetch_google_results', return_value=['https://www.example.com']):
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer valid_key'
        }
        response = test_app.post('/', headers=headers, json={'query': 'test query'})

        assert response.headers['Content-Security-Policy'] == "default-src 'self'"
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        assert response.headers['X-Frame-Options'] == 'DENY'
        assert response.headers['X-XSS-Protection'] == '1; mode=block'

        evil_headers = {
            'X-Frame-Options': 'ALLOW-FROM evil.com'
        }
        response = test_app.post('/', headers={**headers, **evil_headers}, json={'query': 'test query'})
        assert response.headers['X-Frame-Options'] == 'DENY'
