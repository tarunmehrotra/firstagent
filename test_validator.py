from app.database.validator import validate_sql


queries = [
    "delete * FROM dbo.Emp",
    "SELECT AVG(salary) FROM dbo.Emp"
]


for query in queries:

    try:

        validated = validate_sql(query)

        print("VALID:")
        print(validated)

    except ValueError as e:

        print("INVALID:")
        print(e)