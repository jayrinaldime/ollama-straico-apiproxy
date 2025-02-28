from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv()

import asyncio


# pip install browser-use
# install playwright:
# playwright install

# Requires Vision / Image Input capability
#llm_openai = ChatOpenAI(model="openai/gpt-4o-2024-11-20", base_url="http://127.0.0.1:3216/v1", api_key="aawederr")
llm_ollama = ChatOllama(model="openai/gpt-4o-mini", base_url="http://127.0.0.1:3216")

async def main():
    initial_actions = [
        {'open_tab': {'url': 'https://www.google.com'}},
    ]
    agent = Agent(
        task="What is the latest version of python programming langauge",
        llm=llm_ollama,
        initial_actions=initial_actions,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())