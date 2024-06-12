import requests
from agentDVerse import Agent
from dotenv import load_dotenv

load_dotenv()


def search_festival(x):
    json_message = {
        "message": x.get("content")[0].get("message")
    }

    result = requests.post("http://localhost:8000/", json=json_message).json().get("message")

    agent.send_response_to_next(
        initial=x,
        message={
            "message": result
        }
    )


if __name__ == "__main__":
    agent = Agent(
        name="Festival Information Agent",
        description="This agent provides information about upcoming festivals.",
        topics=["festival", "party", "festival-information"],
        output_format="text",
        callback=search_festival
    )
