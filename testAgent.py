import asyncio
import os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain.agents.react.agent import create_react_agent
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
            template = '''Apply the following instructions as best you can. You have access to the following tools to command a running FreeCAD instance:

{tools}

Use the following format:

Instruction: the input instruction you must follow
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Action: invoke the tools and report the result message

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

            prompt = PromptTemplate.from_template(template)
            agent = create_react_agent(model, tools, prompt)
            input_data = {
                "input": "create a box positioned at (0, 0, 0)",
                "chat_history": [], # Optional, but often used
                "intermediate_steps": [],
            }
            fc_response = await agent.ainvoke(input_data)
            print(fc_response)

            input_data = {
                "input": "proceed and report response",
                "chat_history": [], # Optional, but often used
                "intermediate_steps": [],
            }
            fc_response = await agent.ainvoke(input_data)
            print(fc_response)

            input_data = {
                "input": "proceed and report response",
                "chat_history": [], # Optional, but often used
                "intermediate_steps": [],
            }
            fc_response = await agent.ainvoke(input_data)
            print(fc_response)

if __name__ == "__main__":
    asyncio.run(main())