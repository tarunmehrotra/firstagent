from app.database.sql_client import execute_query


query = """
SELECT TOP 10 *
FROM dbo.employee
"""


rows = execute_query(query)

for row in rows:
    print(dict(row))