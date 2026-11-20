from sql_generator import generate_sql
from query_executor import execute_query
from llm import ask_llm


def explain_result(question, sql, columns, rows):
    prompt = f"""
You are an AI business data analyst.

Answer the user's question using only the database result provided below.

Your job is not merely to repeat the rows. Interpret the result and identify
the most useful business observations that are directly supported by the data.

RULES:
- Do not invent facts that are not present in the result.
- Do not claim causation unless the data supports it.
- Clearly distinguish facts from interpretation.
- Mention relevant filters or scope, such as delivered orders.
- Highlight rankings, meaningful differences, patterns, or concentrations
  when they can be calculated from the provided result.
- Do not speculate about why a pattern occurred unless the available data supports it.
- Do not suggest causes such as customer preferences, marketing, seasonality,
  or product quality unless those causes are directly supported by the result.
- Use readable category names instead of database-style underscores.
- Use appropriate number formatting.
- Do not use Markdown bold formatting.

Structure the answer as:
1. A direct answer to the question.
2. Two or three useful observations supported by the result.
3. A short note about important scope or limitations if relevant.

USER QUESTION:
{question}

SQL USED:
{sql}

COLUMNS:
{columns}

DATABASE RESULT:
{rows}
"""

    return ask_llm(prompt)


def answer_question(question):
    sql = generate_sql(question)

    if sql.strip() == "CANNOT_ANSWER":
        return {
            "answer": (
                "The available data cannot answer this question reliably. "
                "The dataset can show purchasing behaviour and related patterns, "
                "but it does not contain direct evidence about customer motivations."
            ),
            "sql": None,
            "columns": None,
            "rows": None,
        }

    columns, rows = execute_query(sql)

    explanation = explain_result(
        question,
        sql,
        columns,
        rows
    )

    return {
        "answer": explanation,
        "sql": sql,
        "columns": columns,
        "rows": rows,
    }
