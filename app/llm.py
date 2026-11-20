import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

model = os.getenv("LLM_MODEL")


def ask_llm(prompt):
    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text