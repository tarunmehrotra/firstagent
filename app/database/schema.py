from app.database.sql_client import execute_query


def get_database_schema():

    query = """
    SELECT
        TABLE_SCHEMA,
        TABLE_NAME,
        COLUMN_NAME,
        DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
    """

    rows = execute_query(query)

    schema = {}

    for row in rows:

        table_name = f"{row['TABLE_SCHEMA']}.{row['TABLE_NAME']}"

        if table_name not in schema:
            schema[table_name] = []

        schema[table_name].append({
            "column": row["COLUMN_NAME"],
            "data_type": row["DATA_TYPE"]
        })

    return schema