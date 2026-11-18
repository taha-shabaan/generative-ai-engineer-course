from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

# 01-laod env variable
load_dotenv()

# 02 init llm model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# 03-request  prompt
messages = [{
    "role":"user",
    "content":"what do you think about ai engineer carear in saudi arabia?"
}]

# 04 create agent
agent = create_agent(model=llm)

# 05- invoke message
response = agent.invoke({"messages":messages})


print(response['messages'][-1].content[0]['text'])
