from googlesearch import search
from dotenv import load_dotenv
import os
import sentry_sdk
from agentDVerse import Agent

load_dotenv()

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


def fetch_google_results(query):
    try:
        return list(search(query, num_results=3))
    except Exception as e:
        print("An error occurred:", e)
        return []


def callback(x):
    result = fetch_google_results(x.get("content")[0].get("message"))
    print(result)

    agent.send_response_to_next(
        initial=x,
        message={
            "message": result
        }
    )


if __name__ == '__main__':
    agent = Agent(
        name="Google Search Agent",
        description="A simple agent that fetches search results from Google",
        topics=["search", "google"],
        output_format="json",
        callback=callback
    )
