"""
Show how to connect to MCP servers that use either SSE or Streamable HTTP transport using our MCPTools and MultiMCPTools classes.

Check the README.md file for instructions on how to run these examples.
"""

import asyncio

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.mcp import MCPTools, MultiMCPTools

# This is the URL of the MCP server we want to use.
server_url = "http://localhost:9875/mcp"


async def run_agent(message: str) -> None:
    async with MCPTools(transport="streamable-http", url=server_url) as mcp_tools:
        agent = Agent(
            model=DeepSeek(id="deepseek-chat"),
            tools=[mcp_tools],
            markdown=True,
        )
        await agent.aprint_response(message=message, stream=True, markdown=True)


# Using MultiMCPTools, we can connect to multiple MCP servers at once, even if they use different transports.
# In this example we connect to both our example server (Streamable HTTP transport), and a different server (stdio transport).
async def run_agent_with_multimcp(message: str) -> None:
    async with MultiMCPTools(
        commands=["npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"],
        urls=[server_url],
        urls_transports=["streamable-http"],
    ) as mcp_tools:
        agent = Agent(
            model=DeepSeek(id="deepseek-chat"),
            tools=[mcp_tools],
            markdown=True,
        )
        await agent.aprint_response(message=message, stream=True, markdown=True)


if __name__ == "__main__":
    asyncio.run(run_agent("Create a box in a new document."))

