"""
MCP Streamable Http Client Usage Example

This script demonstrates how to use the MCPClient to interact with an MCP endpoint,
list available tools, and invoke a tool with parameters.
"""

import argparse
import asyncio
import importlib
import json
import sys
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

def format_result(result):
    content = result.content
    if not result.isError :
        print("Success")
        for cont in content:
            if cont.type == "text":
                print(cont.text)
            elif cont.type == "image":
                print(cont.data, cont.mimeType)
    else:
        print("Failure")
        for cont in content:
            if cont.type == "text":
                print(cont.text)


async def main(section_mod):
    print("Starting MCPClient ...")

    # Connect to a streamable HTTP server
    async with streamablehttp_client("http://localhost:9875/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # Call tools
            tasks = asyncio.gather(section_mod.call_tools(session))
            await tasks

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("section")
    args = parser.parse_args()
    section_mod = importlib.import_module(args.section+"Test")

    asyncio.run(main(section_mod))
    print("Script completed.")
