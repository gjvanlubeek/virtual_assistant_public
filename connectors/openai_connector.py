import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class DigitalBrain(object):
    def __init__(self, job_discription):
        self.model = "gpt-3.5-turbo-1106"
        self.hire_employee = job_discription
        self.conversation = []
        self.conversation.append(
            {"role": "system", "content": self.hire_employee})

    def generate_response(self, question):
        self.question = question
        self.conversation.append({"role": "user", "content": self.question})
        response = client.chat.completions.create(
            model=self.model,
            messages=self.conversation,
            temperature=0.2  # You can adjust this value as needed
        )
        result = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": result})

        return result

    def insert_data_list(self, own_data):
        for data in own_data:
            self.conversation.append({"role": "assistant", "content": data})

    def insert_data(self, data):
        self.conversation.append({"role": "assistant", "content": data})


if __name__ == '__main__':
    va = DigitalBrain("act as a virtual assistant")
    response = va.generate_response("tell a joke")
    print(response)
