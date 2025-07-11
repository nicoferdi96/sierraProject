import os
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

from sierraproject.tools.mcp_config import get_stagehand_mcp_tools

# Load environment variables
load_dotenv()


@CrewBase
class SierraCrew:
    """Sierra Login Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    agents: List[BaseAgent]
    tasks: List[Task]
    mcp_adapter = None
    tools = []

    def __init__(self):
        """Initialize the crew with MCP tools."""
        # Load environment variables
        load_dotenv()
        
        # Initialize MCP adapter
        self.mcp_adapter = get_stagehand_mcp_tools()
        self.tools = self.mcp_adapter.tools
        
        print(f">>> Available tools from Stagehand MCP server: {[tool.name for tool in self.tools]}")

    @agent
    def login_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["login_agent"],  # type: ignore[index]
            tools=self.tools,
            verbose=True,
        )

    @agent
    def summarize_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summarize_agent"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def login_to_sierra(self) -> Task:
        return Task(
            config=self.tasks_config["login_to_sierra"],  # type: ignore[index]
        )

    @task
    def summarize(self) -> Task:
        return Task(
            config=self.tasks_config["summarize"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Login Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
