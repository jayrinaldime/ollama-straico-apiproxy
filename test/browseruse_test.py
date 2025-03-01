from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from browser_use import Agent
from dotenv import load_dotenv

load_dotenv()

import asyncio

# Setup
# Reference: https://docs.browser-use.com/quickstart
# pip install browser-use
# install playwright:
# playwright install

# Requires Vision / Image Input capability
"anthropic/claude-3.7-sonnet"  # OK
"openai/gpt-4o-mini"  # OK
llm_openai = ChatOpenAI(
    model="openai/gpt-4o-mini", base_url="http://127.0.0.1:3214/v1", api_key="aawederr"
)

"anthropic/claude-3.7-sonnet"  # OK
"openai/gpt-4o-mini"  # OK
llm_ollama = ChatOllama(model="openai/gpt-4o-mini", base_url="http://127.0.0.1:3214")


async def main():
    # initial_actions = [
    #     {'open_tab': {'url': 'https://www.google.com'}},
    # ]
    agent = Agent(
        task="What is the latest version of python programming langauge",
        llm=llm_openai,
        # initial_actions=initial_actions,
        # straico api does not support vision only the web platform support vision.
        use_vision=False,
    )
    result = await agent.run()
    print(result)


asyncio.run(main())
