from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, current_time, retrieve, use_aws

# User question to start
user_question = "Find all the ec2 instances in us-east-1, and give me their IPs and AZs in a table."

# Receive user prompt for full conversation
def get_user_input(prompt="Enter your question (or 'exit' to quit): "):
    """Get input from the user with a custom prompt."""
    return input(prompt)

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

# Configure bedrock model
bedrock_model = configure_bedrock_model()

agent_tools = [calculator, current_time, retrieve, use_aws]

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