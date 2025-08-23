# Global imports
import os
# Strands
from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, current_time, retrieve, use_aws
from strands.tools.mcp.mcp_client import MCPClient
# MCP
from mcp.client.streamable_http import streamablehttp_client

# User question to start
user_question = "Tell me about the Repos I own."

# Receive user prompt for full conversation
def get_user_input(prompt="Enter your question (or 'exit' to quit): "):
    """Get input from the user with a custom prompt."""
    return input(prompt)

# Build GitHub MCP
def github_streamable_mcp_client():
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is not set")
    return MCPClient(lambda: streamablehttp_client(
        "https://api.githubcopilot.com/mcp/",
        headers={"Authorization": f"Bearer {token}"}
    ))
  
# Configure bedrock model
def configure_bedrock_model():
    """Configure and return the Bedrock model."""
    return BedrockModel(
        model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
        additional_request_fields={
            "thinking": {
                "type": "enabled",
                "budget_tokens": 1024,  # Minimum of 1,024
            }
        }
    )

# Create agent
def create_agent(agent_tools):
    """Create and return an agent with the given model, system prompt, and tools."""
    return Agent(
        model=bedrock_model,
        tools=agent_tools,
    )

###
## Begin
###

# Create MCP clients
github_mcp_client = github_streamable_mcp_client()

# Open tools and start chatting
with github_mcp_client:

    # Configure bedrock model
    bedrock_model = configure_bedrock_model()

    # Inventory tools each MCP provides
    github_tools = github_mcp_client.list_tools_sync()
    agent_tools = [calculator, current_time, retrieve, use_aws] + github_tools

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