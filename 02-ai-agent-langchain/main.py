from langchain.chat_models import init_chat_model

import os

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

# 1. Initialize the chat model
model = init_chat_model(
    model="gemini-3.8-flash",
    model_provider="google_genai",
    api_key=GOOGLE_API_KEY
    # max_token,
)

# open file
with open('oops.txt') as file:
    op = file.read()
# 2. Invoke the model with a prompt
response = model.invoke(f"whati is best oppurnities for the future  {op}?")


# 3. Print the text content
print(response.content[0]['text'])
