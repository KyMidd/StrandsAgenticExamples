# Global imports
from json import tool
import os
# MCP
from mcp.client.streamable_http import streamablehttp_client
from mcp import stdio_client, StdioServerParameters
# Strands
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from strands.models import BedrockModel
from strands_tools import calculator, current_time
# Logging
import logging

# User question to start
user_question = "Find all active issues over the last 4 hours, find critical outages, and research potential code changes that caused those issues."

# Receive user prompt for full conversation
def get_user_input(prompt="Enter your question (or 'exit' to quit): "):
    """Get input from the user with a custom prompt."""
    return input(prompt)

# Build PagerDuty MCP
def build_pagerduty_mcp_client():
    """Build and return a PagerDuty MCP client."""
    return MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="uv", 
            args=[
                "run",
                "--directory",
                "/Users/kyler/git/GitHub/PagerDuty/pagerduty-mcp-server",
                "python",
                "-m",
                "pagerduty_mcp"
                #"--enable-write-tools"  # This flag enables write operations on the MCP Server enabling you to create issues, pull requests, etc.
            ],
            env={
                "PAGERDUTY_HOST": "https://api.practicefusion.pagerduty.com",
                "PAGERDUTY_USER_API_KEY": os.getenv("PAGERDUTY_USER_API_KEY")
            },
        )
    ))

# Configure bedrock model
def configure_bedrock_model():
    """Configure and return the Bedrock model."""
    return BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        additional_request_fields={
            "thinking": {
                "type": "enabled",
                "budget_tokens": 4096,  # Minimum of 1,024
            }
        }
    )

# Create agent
def create_agent(agent_tools):
    """Create and return an agent with the given model, system prompt, and tools."""
    return Agent(
        model=bedrock_model,
        tools=agent_tools
    )

# Create MCP clients
pagerduty_mcp_client = build_pagerduty_mcp_client()

# Open tools and start chatting
with pagerduty_mcp_client:

    # Configure bedrock model
    bedrock_model = configure_bedrock_model()

    # Inventory tools each MCP provides
    pagerduty_tools = pagerduty_mcp_client.list_tools_sync()
    agent_tools = pagerduty_tools + [calculator, current_time]

    # Create agent with tools
    agent = create_agent(agent_tools)

    # Begin conversation loop
    while True:
        print("User question:", user_question, end="\n\n")
        
        # Get response from agent
        response = agent(user_question)
        print("-" * 50)
        
        # Ask for follow-up question
        user_question = get_user_input("Question for model (or 'exit' to exit): ")
        if user_question.lower() == 'exit':
            break
        print("-" * 50)