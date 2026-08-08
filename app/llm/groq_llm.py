from groq import Groq
from app.config.settings import settings


client = Groq(api_key=settings.groq_api_key)


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