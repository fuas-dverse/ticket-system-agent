import os
import sys
import pytest

# Append the directory above 'tests/' to the path to find 'app.py'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # Now it should recognize 'app'


@pytest.fixture()
def test_app():
    # If your Flask app is not already using a test configuration, you can configure it here
    app.config.update({
        'TESTING': True,
        'DEBUG': True,
    })

    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context before running the tests
        with app.app_context():
            yield testing_client  # this is where the testing happens
