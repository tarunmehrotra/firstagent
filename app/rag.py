from app.retrival.retriever import retrieve
from app.llm.groq_llm import generate_answer


def ask_question(query: str):

    results = retrieve(query, top_k=5)

    context = "\n\n".join(
        result.metadata.get("text", "")
        for result in results
    )

    answer = generate_answer(
        query=query,
        context=context
    )

    return answer