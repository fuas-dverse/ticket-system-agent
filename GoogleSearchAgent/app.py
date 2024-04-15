from googlesearch import search
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_API_KEY = os.getenv('API_KEY')

app = Flask(__name__)


def fetch_google_results(query):
    try:
        return list(search(query, num_results=3))
    except Exception as e:
        print("An error occurred:", e)
        return []


def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        if request.headers.get('key') and request.headers.get('key') == SECRET_API_KEY:
            return view_function(*args, **kwargs)
        else:
            abort(401)  # Unauthorized access

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


if __name__ == '__main__':
    app.run(port=5002, debug=True)
