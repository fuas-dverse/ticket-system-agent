# Import necessary modules
from googlesearch import search
from dotenv import load_dotenv
from agentDVerse import Agent

# Load environment variables from .env file
load_dotenv()


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
    # Create an instance of the Agent class
    agent = Agent(
        name="Google Search Link Agent",
        description="A simple agent that fetches search results from Google and returns a list of URLs.",
        topics=["search", "google", "links", "urls"],
        output_format="json",
        callback=callback
    )
