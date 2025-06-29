
import json
import logging
from rasa.core.agent import Agent

# Load pre-trained Rasa model
agent = Agent.load("models/nlu.tar.gz")

def lambda_handler(event, context):
    user_input = event.get("query", "")
    result = agent.parse_message(user_input)
    top_intent = result.get("intent", {}).get("name", "")
    
    if top_intent == "CancelTimer":
        logging.info("Intent recognized: CancelTimer")
        return {
            "statusCode": 200,
            "body": json.dumps({"response": "Timer cancelled"})
        }
    return {
        "statusCode": 200,
        "body": json.dumps({"response": "Intent not recognized"})
    }
