from app.retrival.retriever import retrieve


query = "What is the mileage of Tata Nexon?"

results = retrieve(query, top_k=5)

print("\nQuery:", query)
print("\nTop Results:\n")

for i, result in enumerate(results, 1):
    print(f"Result {i}")
    print("Score:", result.score)
    print("Metadata:", result.metadata)
    print("-" * 80)