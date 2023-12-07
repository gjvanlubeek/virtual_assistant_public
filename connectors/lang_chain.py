import os
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
chat_models = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful english AI bot. Your name is {name}."),
        ("human", "Hello, how are you doing?"),
        ("ai", "I'm doing well, thanks!"),
        ("human", "{user_input}"),
    ]
)

messages = chat_template.format_messages(name="Dorothy", user_input="What is your name?")

replay = chat_models.invoke(messages)

print(replay.content)
