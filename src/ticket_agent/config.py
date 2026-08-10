from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseModel):
    connection_uri: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URI",
    )
    database_name: str = Field(default="ticket_agent", description="MongoDB database name")
    kb_collection: str = Field(default="knowledge_base", description="KB collection name")
    ticket_collection: str = Field(default="tickets", description="Historical tickets collection name")


class ServiceNowSettings(BaseModel):
    instance_url: str = Field(
        default="https://dev12345.service-now.com",
        description="ServiceNow instance URL",
    )
    username: str = Field(description="ServiceNow username")
    password: str = Field(description="ServiceNow password")


class LLMSettings(BaseModel):
    cohere_api_key: str = Field(description="Cohere API key")
    cohere_api_model: str = Field(default="command-r-plus", description="Cohere model name")
    temperature: float = Field(default=0.2, description="LLM sampling temperature")


class QueueSettings(BaseModel):
    aws_region: str = Field(default="us-east-1", description="AWS region")
    aws_access_key_id: str = Field(description="AWS access key ID")
    aws_secret_access_key: str = Field(description="AWS secret access key")
    sqs_queue_url: str = Field(description="SQS queue URL")
    sqs_queue_name: str = Field(description="SQS queue name")
    sqs_dlq_url: str = Field(description="SQS dead-letter queue URL")
    poll_interval_seconds: int = Field(default=10, description="Queue poll interval in seconds")


class AppSettings(BaseModel):
    log_level: str = Field(default="INFO", description="Logging level")
    environment: str = Field(default="dev", description="Environment: dev, staging, prod")
    max_retries: int = Field(default=3, description="Max retry attempts for external calls")
    retry_backoff_seconds: float = Field(default=2.0, description="Base backoff time between retries")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    mongo: MongoSettings = Field(default_factory=MongoSettings)
    servicenow: ServiceNowSettings
    llm: LLMSettings
    queue: QueueSettings
    app: AppSettings = Field(default_factory=AppSettings)


settings = Settings()