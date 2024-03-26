import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv('GROQ_API_KEY')

client = Groq(
    api_key=os.getenv('GROQ_API_KEY'),
)

user_input = input("Please type a prompt: ")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a helpfull quote generator who writes tweets about love."
        },
        {
            "role": "user",
            "content": user_input
        }
    ],
    model="mixtral-8x7b-32768",
    max_tokens=1024,
    temperature=0.5,
    top_p=1,
    stop=None,
    stream=False,
)

print(chat_completion.choices[0].message.content)