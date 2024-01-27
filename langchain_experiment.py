import os
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

from langchain.prompts import PromptTemplate

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
llm  = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo-1106")

prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?, add a discription for this company name, 2000 words")
message = prompt.format(product="fish")

for i in range(1):
    print(llm.invoke(message).content)