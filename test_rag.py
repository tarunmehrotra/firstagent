from app.rag import ask_question


query = "When did india announced a lockdown in covid?"

answer = ask_question(query)

print("\nQuestion:")
print(query)

print("\nAnswer:")
print(answer)