import requests
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

@tool
def calculator(expression):
    """
    This calculator function solves any arthmaticc expression containing all constant values.
    It supports addition, subtraction, multiplication, division, exponentiation and parentheses.

    :param expression: str: The arithmetic expression
    :return: str: The result as str
    """
    try:
        result = eval(expression)
        result = str(result)
    except:
        result = "Error: Cannot solve expression"

llm= init_chat_model(
    model = "google/gemma-3n-e4b",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "non-needed"
)

agent = create_agent(
    model=llm,
    tools=[calculator],
    system_prompt="You are a helpful assistant. Answer in short."
)

while True:
    user_input = input("You: ")
    if user_input == "exit":
        break
    result = agent.invoke({"messages": [
        {"role": "user", "content": user_input}
    ]})
    llm_output = result["messages"][-1]
    print("AI: ", llm_output.content)
    print("\n\n",result["messages"])
