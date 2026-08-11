from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from app.rag import ask_question
from app.agents.sql_agent import execute_sql_question

app = FastAPI(
    title="RAG Agent API",
    description="Multi-source RAG application using PDF, SQL Server and Groq",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ask")
def ask(question: str):

    # Temporary router
    question_lower = question.lower()

    sql_keywords = [
        "employee",
        "employees",
        "salary",
        "product",
        "products",
        "count",
        "average",
        "avg",
        "database",
        "sql",
        "table",
        "customer",
        "customers"
    ]

    if any(keyword in question_lower for keyword in sql_keywords):

        answer = execute_sql_question(question)

        return {
            "question": question,
            "source": "sql",
            "answer": answer
        }

    else:

        answer = ask_question(question)

        return {
            "question": question,
            "source": "pdf",
            "answer": answer
        }


@app.get("/ask-sql")
def ask_sql(question: str):

    answer = execute_sql_question(question)

    return {
        "question": question,
        "source": "sql",
        "answer": format_sql_answer(answer)
    }
    import json


def format_sql_answer(answer):
    """
    Convert SQL Agent output into readable text.
    """

    # Already a normal string
    if isinstance(answer, str):

        # Try to parse JSON string
        try:
            parsed = json.loads(answer)
            return format_sql_answer(parsed)
        except:
            return answer

    # List of rows
    if isinstance(answer, list):

        if not answer:
            return "No records found."

        lines = []

        for row in answer:

            if isinstance(row, dict):

                # Handle single-column results
                if len(row) == 1:
                    value = list(row.values())[0]

                    if value is None:
                        value = "N/A"

                    lines.append(str(value))

                # Handle multiple-column results
                else:
                    values = []

                    for key, value in row.items():

                        if value is None:
                            value = "N/A"

                        values.append(
                            f"{key}: {value}"
                        )

                    lines.append(" | ".join(values))

            else:
                lines.append(str(row))

        return "\n".join(lines)

    # Dictionary
    if isinstance(answer, dict):

        lines = []

        for key, value in answer.items():

            if value is None:
                value = "N/A"

            lines.append(
                f"{key}: {value}"
            )

        return "\n".join(lines)

    return str(answer)