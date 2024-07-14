import requests
from os import environ
from app import logging

logger = logging.getLogger(__name__)

STRAICO_API_KEY = environ["STRAICO_API_KEY"]
logger.info(f"STRAICO_API_KEY={STRAICO_API_KEY}")
def prompt_completion(msg: str, model: str= "openai/gpt-3.5-turbo-0125") -> str:
    r = requests.post("https://api.straico.com/v0/prompt/completion",
              headers = {"Authorization": f"Bearer {STRAICO_API_KEY}"},
              data = {"model": model,
                      "message": msg})
    return r.json()["data"]["completion"]["choices"][-1]["message"]["content"]


def list_model():
    r = requests.get("https://api.straico.com/v0/models",
                     headers={"Authorization": f"Bearer {STRAICO_API_KEY}"}, )
    return r.json()

