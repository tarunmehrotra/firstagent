from app.agents.sql_agent import execute_sql_question


question = "What is the average salary of employees?"

result = execute_sql_question(question)

print("\nQuery Result:")

for row in result:
    print(dict(row))