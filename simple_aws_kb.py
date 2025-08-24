from strands import Agent
from strands_tools import retrieve
agent = Agent(tools=[retrieve])
agent("Tell me about the cloud platform team")