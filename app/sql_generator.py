from llm import ask_llm
from sql_validator import validate_sql


def load_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


business_definitions = load_file("config/business_definitions.md")
data_model = load_file("config/data_model.md")


def generate_sql(question):
    prompt = f"""
You are an AI data analyst.

Your task is to convert the user's business question into PostgreSQL SQL.

BUSINESS DEFINITIONS:

{business_definitions}

DATA MODEL:

{data_model}

RULES:

- Use only the approved analytical views described in the data model.
- Never query raw Olist tables.
- Generate read-only SQL only.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, or other modifying statements.
- Return only SQL.
- Do not include Markdown code fences.
- If the question cannot be answered from the available data, return:
  CANNOT_ANSWER

USER QUESTION:

{question}
"""

    return ask_llm(prompt)
