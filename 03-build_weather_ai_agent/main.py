from langchain.tools import tool
from langchain.agents import create_agent
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
from dotenv import load_dotenv


load_dotenv()

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city: Name of the city, e.g. "London" or "Cairo".

    Returns:
        A short description of the current weather and temperature.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
    }
    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    condition = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    return f"Weather in {city} is {condition}, and the temperature is {temperature}°C."


if __name__ == "__main__":
    query = input("Enter your query: ")

    system_prompt = """
    You are a helpful weather expert.
    When asked about the weather in a city, use your weather tool to get the current data and always respond in this exact format:
    Weather in {city} is {condition}, and the temperature is {temperature}.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        max_tokens=1000,
        timeout=None,
        max_retries=2,
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    agent = create_agent(
        model=llm,
        tools=[get_weather],
        system_prompt=system_prompt,
    )

    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    print(result["messages"][-1].content)
