import asyncio
import os
import sys
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai.chat_models.base import BaseChatOpenAI
from langchain_core.prompts import PromptTemplate

async def main():

    async with streamablehttp_client("http://localhost:9875/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            model = BaseChatOpenAI(
                    model='deepseek-chat',
                    openai_api_key=os.environ.get("DEEPSEEK_API_KEY"),
                    openai_api_base='https://api.deepseek.com',
                    max_tokens=1024
            )
            # Get tools
            tools = await load_mcp_tools(session)
            tool_names = []
            for t in tools:
                tool_names.append(t.name)

            agent = create_react_agent(model, tools)
            input_data = {
                "messages": [{"role": "system", "content": "You are in command of a running FreeCAD 1.0 instance."}, 
                              {"role": "user", "content": "Create a box with dimensions 10x10x10 positioned at (100, 100, 100) in a new document named 'BoxDocument'"}]
            }
            fc_response = await agent.ainvoke(input_data)
            print(fc_response)



if __name__ == "__main__":
    asyncio.run(main())