from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

from app.config.settings import settings


def get_sql_engine():

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={settings.sql_server};"
        f"DATABASE={settings.sql_database};"
        f"UID={settings.sql_username};"
        f"PWD={settings.sql_password};"
        "TrustServerCertificate=yes;"
    )

    connection_url = (
        "mssql+pyodbc:///?odbc_connect="
        + quote_plus(connection_string)
    )

    engine = create_engine(connection_url)

    return engine


def execute_query(query: str):

    engine = get_sql_engine()

    with engine.connect() as connection:

        result = connection.execute(text(query))

        rows = result.mappings().all()

    return rows