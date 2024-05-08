import pytest
import requests_mock
from pytest_benchmark.plugin import benchmark
from app import search_hotels
from init import download_nltk_data


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture(scope="session")
def install_packages():
    download_nltk_data()


def test_search_hotel_benchmark(benchmark, mock_requests):
    mock_requests.get('https://booking-com.p.rapidapi.com/v1/hotels/locations', json=[{"dest_id": "123", "dest_type": "city"}])
    mock_requests.get('https://booking-com.p.rapidapi.com/v1/hotels/search', json={"result": [{"hotel_name": "Hotel1", "address": "Address1", "review_score_word": "Good", "min_total_price": "100", "url": "url1", "main_photo_url": "url1"}]})

    result = benchmark(search_hotels, 'I want to book a hotel in Spain')

    assert benchmark.stats['mean'] < 0.5, "Benchmark is too slow"


def test_search_hotel_benchmark_no_city(benchmark, mock_requests):
    mock_requests.get('https://booking-com.p.rapidapi.com/v1/hotels/locations', json=[{"dest_id": "123", "dest_type": "city"}])
    mock_requests.get('https://booking-com.p.rapidapi.com/v1/hotels/search', json={"result": [{"hotel_name": "Hotel1", "address": "Address1", "review_score_word": "Good", "min_total_price": "100", "url": "url1", "main_photo_url": "url1"}]})

    result = benchmark(search_hotels, 'I want to book a hotel')

    assert benchmark.stats['mean'] < 2, "Benchmark is too slow"
