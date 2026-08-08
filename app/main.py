from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.rag import ask_question


app = FastAPI(
    title="RAG Agent API",
    description="PDF-based RAG application using Pinecone and Groq",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "RAG Agent API is running"
    }


@app.get("/ask")
def ask(question: str):
    answer = ask_question(question)

    return {
        "question": question,
        "answer": answer
    }