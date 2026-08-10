import re


def validate_sql(query: str) -> str:

    query = query.strip()

    # Remove markdown code fences if LLM returns them
    query = re.sub(r"```sql", "", query, flags=re.IGNORECASE)
    query = query.replace("```", "").strip()

    # Only allow SELECT queries
    if not query.lower().startswith("select"):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    # Block dangerous SQL operations
    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "merge",
        "exec",
        "execute"
    ]

    query_lower = query.lower()

    for keyword in forbidden_keywords:

        if re.search(
            rf"\b{keyword}\b",
            query_lower
        ):
            raise ValueError(
                f"Forbidden SQL operation detected: {keyword}"
            )

    return query