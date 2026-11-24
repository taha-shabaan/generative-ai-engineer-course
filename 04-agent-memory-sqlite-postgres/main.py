from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.tools import tool
import requests
import os

# Load environment variables
load_dotenv()

# Define weather tool
@tool
def get_weather(city: str):
    """Get the current weather for a given city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY not found in environment variables."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unknown error')}"
        return f"{city}: {data['weather'][0]['description']}, {data['main']['temp']}°C, feels like {data['main']['feels_like']}°C"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


@tool
def get_location():
    """
      function return curretn location for the user
    """
    location_url ="https://ipapi.co/json"
    response=requests.get(location_url)
    data = response.json()
    print(data)
    return f"city:.. and country:from {data}"


@tool
def get_city_time(city: str):
    """Get the current time for a given city."""
    return f"Current time in {city}: (placeholder - integrate with worldtime API)"


# Initialize LLM gemma-4
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    max_tokens=500,
    timeout=None,
    max_retries=2,
)

# System prompt
system_prompt = """
You are a helpful weather assistant.
Use the available tools to get weather information for cities around the world.
Use the available tools to get the current user's location and return with the same output.
"""
# with SqliteSaver.from_conn_string('checkpoints.db') as checkpointer:
#     agent = create_agent(
#         model=llm,
#         tools=[get_weather, get_location],
#         system_prompt=system_prompt,
#         checkpointer=checkpointer
#     )

# persistence data with sqlite

if __name__=="__main__":
    with SqliteSaver.from_conn_string("data.db") as checkpointer:
        # Create agent
        agent = create_agent(
            model=llm,
            tools=[get_weather, get_city_time, get_location],
            system_prompt=system_prompt,
            checkpointer=checkpointer
        )
        # Interactive loop
        print("Weather AI Agent ready! Type 'exit' to quit.")
        while True:
            user_input = input("\nEnter city name: ")
            if user_input.lower() in ["exit", "quit"]:
                break


            messages = [{"role": "user", "content": user_input}]
            thread_config = {"configurable": {"thread_id": "1"}}
            response = agent.invoke({"messages": messages}, thread_config)
            print("\n" + response['messages'][-1].content[0]['text'])
