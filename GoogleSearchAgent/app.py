from googlesearch import search
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
import os
import sentry_sdk
load_dotenv()

SECRET_API_KEY = os.getenv('API_KEY')
SENTRY_KEY = os.getenv('SENTRY_DSN')

sentry_sdk.init(
    dsn=SENTRY_KEY,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)


def fetch_google_results(query):
    try:
        return list(search(query, num_results=3))
    except Exception as e:
        print("An error occurred:", e)
        return []


def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        expected_key = os.getenv('API_KEY')  # Make sure this matches your environment config
        provided_key = request.headers.get('Authorization')
        if not provided_key or provided_key != f'Bearer {expected_key}':
            abort(401)  # Unauthorized access
        return view_function(*args, **kwargs)

    return decorated_function


@app.route('/', methods=['POST'])
@require_api_key
def get_response():
    data = request.json
    query = data.get("query")

    if query is None or query == "":
        return jsonify({"error": "You must fill in a search query!"}), 400  # Using 400 for client error

    response = fetch_google_results(query)

    return jsonify({'response': response}), 200


# Adding security headers
@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains'
    return response


if __name__ == '__main__':
    app.run(port=5002)
