    # Import necessary modules
from googlesearch import search
from dotenv import load_dotenv
import os
import sentry_sdk
from agentDVerse import Agent

# Load environment variables from .env file
load_dotenv()

# Get Sentry DSN from environment variables
SENTRY_KEY = os.getenv('SENTRY_DSN')

# Initialize Sentry SDK for error tracking and performance monitoring
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

def fetch_google_results(query):
    """
    Function to fetch Google search results for a given query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of URLs from the search results. Returns an empty list if an error occurs.
    """
    try:
        return list(search(query, num_results=3))
    except Exception as e:
        print("An error occurred:", e)
        return []

def callback(x):
    """
    Callback function to process the search query and send the response.

    Args:
        x (dict): The input data containing the search query.

    Returns:
        None
    """
    result = fetch_google_results(x.get("content")[0].get("message"))
    print(result)

    agent.send_response_to_next(
        initial=x,
        message={
            "message": result
        }
    )

if __name__ == '__main__':
    # Create an instance of the Agent class
    agent = Agent(
        name="Google Search Link Agent",
        description="A simple agent that fetches search results from Google and returns a list of URLs.",
        topics=["search", "google", "links", "urls"],
        output_format="json",
        callback=callback
    )