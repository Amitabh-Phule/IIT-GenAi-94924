# Q1
# • Create tools: calculator, file reader, current weather, and knowledge lookup
# using @tool decorator.
# • Build an agent with all three tools and test with prompts requiring tool usage.
# • Inspect message history to understand tool-calling flow.
# • Implement a logging middleware and observe its output during agent
# execution.


from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call
from dotenv import load_dotenv
import os
import json
import requests

load_dotenv()

# • Create tools: calculator, file reader, current weather, and knowledge lookup
# using @tool decorator.
@tool 
def calculator(expression):
    """
    This calculator function solves any arithmetic expression containing all constant values.
    It supports basic arithmetic operators +, -, *, /, and parenthesis. 
    
    :param expression: str input arithmetic expression
    :returns expression result as str
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"


@tool
def read_file(filepath):
    """Read and return the content of a text file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except :
        return f"Error reading file:"

@tool
def current_weather(city):
    """
    This get_weather() function gets the current weather of given city.
    If weather cannot be found, it returns 'Error'.
    This function doesn't return historic or general weather of the city.

    :param city: str input - city name
    :returns current weather in json format or 'Error'    
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api_key}&units=metric&q={city}"
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    except:
        return "Error"


@tool
def knowledge_lookup(query: str) -> str:
    """Answer general knowledge questions using built-in knowledge."""
    # Simple stub – LLM will answer without external API
    return f"Knowledge lookup query received: {query}"

@wrap_model_call
def logging_middleware(request, handler):
    print("\n--- BEFORE MODEL CALL ---")
    print("Messages sent to model:")
    for msg in request.messages:
        print(msg)

    response = handler(request)

    print("\n--- AFTER MODEL CALL ---")
    print("Model response:")
    print(response.result[0].content)

    return response

llm = init_chat_model(
    model = "google/gemma-3n-e4b",
    model_provider = "openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key = "non-needed"
)
agent = create_agent(
            model=llm, 
            tools=[
                calculator,
                read_file,
                current_weather,
                knowledge_lookup
            ],
            system_prompt="You are a helpful assistant. Use tools when required. Answer briefly."
        )


conversation = []
print("Agent ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    conversation.append({"role": "user", "content": user_input})
    result = agent.invoke({"messages": conversation})
    ai_msg = result["messages"][-1]
    print("\nAI:", ai_msg.content)
    # Inspect full message history
    print("\n--- MESSAGE HISTORY ---")
    for m in result["messages"]:
        print(m)
    conversation = result["messages"]