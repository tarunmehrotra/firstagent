from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
        "answer": answer
    }