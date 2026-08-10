from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    pinecone_api_key: str
    pinecone_index_name: str
    pinecone_namespace: str = "ragproject"


    sql_server: str
    sql_database: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()