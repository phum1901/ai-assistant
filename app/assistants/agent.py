import os
from typing import List, Literal

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

from contextlib import AsyncExitStack

from pydantic import BaseModel, Field
from assistants.prompt import *

class IssueSummaryOutput(BaseModel):
    reported_issues: List[str] = Field(..., description="List of problems or symptoms mentioned in the report")
    affected_features: List[str] = Field(..., description="List of features or components affected by the issue")
    severity: Literal["low", "medium", "high", "critical"] = Field(..., description="Estimated severity level")


async def create_agent():
	common_exit_stack = AsyncExitStack()

	retriever_tools, _ = await MCPToolset.from_server(
		connection_params=SseServerParams(
			url=os.getenv("SSE_URL")
		),
		async_exit_stack=common_exit_stack
	)

	issue_summarizer_agent = Agent(
		model=os.getenv("LLM"),
		name = "summarizer_agent",
		description=SUMMARIZER_DESCRIPTION,
		instruction=SUMMARIZER_INSTRUCTION,
        output_schema=IssueSummaryOutput,
	)

	root_agent = Agent(
		model=os.getenv("LLM"),
		name = "coordinator_agent",
		description=COORDINATOR_DESCRIPTION,
		instruction=COORDINATOR_INSTRUCTION,
		sub_agents=[issue_summarizer_agent],
		tools=[*retriever_tools]
	)
	return root_agent, common_exit_stack 

root_agent = create_agent()