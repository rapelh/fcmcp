# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.tools.mcp_tool.mcp_toolset import MCPTool

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='freecad_adk',
    instruction=f"""\
You are in command of a running FreeCAD 1.0 instance. Execute tools according to the user's orders.
    """,
    tools=[
        MCPTool(
            connection_params=StreamableHTTPServerParams(
                url='http://localhost:9875/mcp',
            ),
            tool_filter=[
            ],
        )
    ],
)
