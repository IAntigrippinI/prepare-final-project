import loguru
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppBaseSettings(BaseSettings):
    COMMON_DB_USERNAME: str
    COMMON_DB_PASSWORD: str
    DB_PORT_PIPELINE: int
    DB_HOSTNAME_PIPELINE: str
    DB_NAME_PIPELINE: str


    model_config = SettingsConfigDict(
        env_file="/opt/airflow/src/.env",
        extra="ignore"
    )


    @property
    def DB_URL(self) -> str:
        return f"postgresql+psycopg2://{self.COMMON_DB_USERNAME}:{self.COMMON_DB_PASSWORD}@{self.DB_HOSTNAME_PIPELINE}:{5432}/{self.DB_NAME_PIPELINE}"

    # @property
    # def DB_URL_MIGRATION(self) -> str:
    #     return f"postgresql+psycopg2://{self.DB_USERNAME_PARSER}:{self.DB_PASSWORD_PARSER}@{self.DB_HOSTNAME_PARSER}:{self.DB_COMMON_PORT}/{self.DB_NAME_PARSER}"



settings = AppBaseSettings()
