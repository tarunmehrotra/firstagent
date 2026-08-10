from groq import Groq
from app.config.settings import settings

client = Groq(api_key=settings.groq_api_key)


# Used by PDF RAG Agent
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

    return response.choices[0].message.content


# Used by SQL Agent
def generate_sql(question: str, schema: str) -> str:

    prompt = f"""
You are an expert SQL Server query generator.

You have access to the following database schema:

{schema}

User question:
{question}

Generate a SQL Server query that answers the user's question.

Rules:
1. Return ONLY the SQL query.
2. Do not use markdown code fences.
3. Do not explain the query.
4. Use ONLY tables and columns from the provided schema.
5. Use SQL Server syntax.
6. Only generate SELECT queries.
7. Never generate INSERT.
8. Never generate UPDATE.
9. Never generate DELETE.
10. Never generate DROP.
11. Never generate ALTER.
12. Never generate TRUNCATE.

SQL query:
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