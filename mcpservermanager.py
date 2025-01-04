import json
from pathlib import Path
import logging
logger = logging.getLogger(__name__)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_settings_filepath = Path("./data/mcp_client/server_settings.json")
if not server_settings_filepath.exists():
    logger.warning("mcp server settings does not exist")

with server_settings_filepath.open("r", encoding="utf-8") as reader:
    server_settings = json.load(reader)

server_mapping = {}
async def initialize_mcp_servers():
    for server_name, server_setting in server_settings.get("mcpServers").items():
        server_params = StdioServerParameters(**server_setting)
        context = stdio_client(server_params)
        read, write = await (context.__aenter__())
        session = ClientSession(read, write)
        #session = await context2.__aenter__()
        # Initialize the connection
        await session.__aenter__()
        await session.initialize()

        server_mapping[server_name] = (session, context)
        logger.info(f"MCP Server {server_name} Launch Complete")

async def close_mcp_servers():
    for server_name, (session, context) in server_mapping.items():
        logger.info(f"MCP Server {server_name} Close")
        await session.__aclose__()
        await context.__aclose__()
