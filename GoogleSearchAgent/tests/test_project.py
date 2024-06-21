import pytest
from unittest.mock import patch, MagicMock
from app import fetch_google_results, callback


# No need for the test_app fixture since it's not a Flask application

@patch('app.search')
def test_fetch_google_results(mock_search):
    mock_search.return_value = ['result1', 'result2', 'result3']
    results = fetch_google_results('test query')
    assert results == ['result1', 'result2', 'result3']

    mock_search.side_effect = Exception('Test exception')
    results = fetch_google_results('test query')
    assert results == []


