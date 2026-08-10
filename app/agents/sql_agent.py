from app.database.schema import get_database_schema
from app.database.validator import validate_sql
from app.database.sql_client import execute_query
from app.llm.groq_llm import generate_sql


def format_schema(schema):

    schema_text = ""

    for table, columns in schema.items():

        schema_text += f"\nTable: {table}\n"

        for column in columns:

            schema_text += (
                f"  - {column['column']} "
                f"({column['data_type']})\n"
            )

    return schema_text


def create_sql_query(question: str):

    schema = get_database_schema()

    schema_text = format_schema(schema)

    sql_query = generate_sql(
        question=question,
        schema=schema_text
    )

    validated_query = validate_sql(sql_query)

    return validated_query


def execute_sql_question(question: str):

    sql_query = create_sql_query(question)

    print("\nGenerated SQL:")
    print(sql_query)

    result = execute_query(sql_query)

    return result