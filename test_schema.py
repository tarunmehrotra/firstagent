from app.database.schema import get_database_schema


schema = get_database_schema()


for table, columns in schema.items():

    print(f"\nTABLE: {table}")

    for column in columns:

        print(
            f"  {column['column']} "
            f"({column['data_type']})"
        )