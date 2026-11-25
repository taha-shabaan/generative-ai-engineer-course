import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.tools import tool
import requests

load_dotenv()
DB_URL = os.getenv("SUPASE_DB_URL")  # Verify spelling in your .env!

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY not found."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unknown error')}"
        return f"{city}: {data['weather'][0]['description']}, {data['main']['temp']}°C, feels like {data['main']['feels_like']}°C"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

@tool
def get_location() -> str:
    """Return the current location."""
    try:
        response = requests.get("https://ipapi.co", headers={"User-Agent": "weather-agent/1.0"}, timeout=10)
        data = response.json()
        return f"City: {data.get('city')}, Country: {data.get('country_name')}"
    except Exception as e:
        return f"Error fetching location: {str(e)}"

@tool
def get_city_time(city: str) -> str:
    """Get the current time for a given city."""
    return f"Current time in {city}: (placeholder - integrate with worldtime API)"

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",  # Update to your exact valid Gemini model ID
    max_tokens=500,
    max_retries=2,
)

system_prompt = """
You are a helpful weather assistant.
Use the available tools to get weather information for cities around the world.
Use the available tools to get the current user's location and return with the same output.
"""

def run_agent(user_input: str, thread_id: str = "1") -> str:
    """Invoke agent with an active Postgres connection and return the reply."""
    if not DB_URL:
        raise ValueError("Database URL is missing from environment variables.")

    with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
        checkpointer.setup()
        agent = create_agent(
            model=llm,
            tools=[get_weather, get_city_time, get_location],
            system_prompt=system_prompt,
            checkpointer=checkpointer,
        )

        messages = [{"role": "user", "content": user_input}]
        thread_config = {"configurable": {"thread_id": thread_id}}
        response = agent.invoke({"messages": messages}, thread_config)

        last_msg = response["messages"][-1].content
        return last_msg[0]["text"] if isinstance(last_msg, list) else str(last_msg)

if __name__=="__main__":
    while True:
        query = input("enter your query.:")
        if query.lower() in ['quit', 'exit', 'bye']:
            break
        print(run_agent(query))
