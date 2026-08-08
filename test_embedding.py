from app.injestion.embedder import create_embedding


text = "Employees are eligible for annual leave."


embedding = create_embedding(text)


print("Embedding created successfully")
print("Vector dimensions:", len(embedding))
print("First 10 values:", embedding[:10])