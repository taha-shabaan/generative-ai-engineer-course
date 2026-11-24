from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.tools import tool

# define tool
@tool
def cities_high_salaries():
    """tell what is city in saudi arabia"""
    return "rayida, jadah, domma ....."

@tool
def find_city_highest_salary():
    """"return city has highest salary please..."""
    return "city name"


# 01-laod env variable
load_dotenv()

# 02 init llm model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    max_tokens=500,
    timeout=None,
    max_retries=2,
    # other params...
)

# 03-system & request  prompt
system_prompt = """"
     you are a helpful assistant in developing.
"""
messages = [{
    "role":"user",
    "content":"what do you think about ai engineer carear in saudi arabia?"
}]

# 04 create agent
agent = create_agent(
    model=llm,
    tools=[cities_high_salaries, find_city_highest_salary],
    system_prompt=system_prompt)

# 05- invoke message
response = agent.invoke({"messages":messages})


print(response['messages'][-1].content[0]['text'])
