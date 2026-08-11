from groq import Groq
from app.config.settings import settings


client = Groq(
    api_key=settings.groq_api_key
)


# =========================================================
# PDF RAG AGENT
# =========================================================

def generate_answer(query: str, context: str) -> str:

    prompt = f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the information provided
in the context below.

If the answer is not available in the context, say:
"I don't have enough information in the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


# =========================================================
# SQL AGENT - GENERATE SQL
# =========================================================

def generate_sql(question: str, schema: str) -> str:

    prompt = f"""
You are an expert SQL Server developer.

Your task is to convert the user's question into a SQL Server query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

IMPORTANT RULES:

1. Generate ONLY the SQL query.
2. Do NOT explain the query.
3. Do NOT return JSON.
4. Do NOT return Python dictionaries.
5. Do NOT use markdown.
6. Do NOT use ```sql.
7. Use SQL Server syntax.
8. Use only tables and columns that exist in the provided schema.
9. For counting rows, use COUNT(*).
10. For average, use AVG().
11. For total, use SUM().
12. For maximum, use MAX().
13. For minimum, use MIN().
14. For listing records, use SELECT.
15. Do not modify the database.
16. Only generate SELECT queries.

Return ONLY the SQL query.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql_query = response.choices[0].message.content.strip()

    # Remove markdown if Groq accidentally returns it
    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")

    return sql_query.strip()


# =========================================================
# SQL AGENT - GENERATE FINAL ANSWER
# =========================================================

def generate_sql_answer(
    question: str,
    sql_query: str,
    result
) -> str:

    prompt = f"""
You are an intelligent SQL data assistant.

Answer the user's question using the SQL query result.

USER QUESTION:
{question}

SQL QUERY:
{sql_query}

SQL RESULT:
{result}

RULES:

1. Give ONLY the final natural-language answer.
2. Do NOT show the SQL query.
3. Do NOT show Python dictionaries.
4. Do NOT show JSON.
5. Do NOT show Decimal().
6. Do NOT show brackets like [] or {{}}.
7. Do NOT mention "Query Result".
8. Do NOT invent information.
9. Use only information contained in the SQL result.
10. If the result contains one value, directly explain that value.
11. If the result contains multiple records, present them as a clean numbered list.
12. If the result is empty, say "No matching records were found."
13. Keep the answer clear and concise.
14. Explain what the returned value means based on the user's question.

Examples:

Question:
What is the average salary of employees?

Result:
[{{'': Decimal('77000.000000')}}]

Answer:
The average salary of employees is 77,000.

Question:
How many employees are there?

Result:
[{{'': 17}}]

Answer:
There are 17 employees.

Question:
Give the names of employees.

Result:
[{{'name': 'Alice'}}, {{'name': 'Bob'}}]

Answer:
1. Alice
2. Bob

Return ONLY the final answer.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()