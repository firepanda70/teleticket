from pydantic_settings import BaseSettings


class Config(BaseSettings):
    bot_token: str
    db_url: str
    log_level: str
    secret: str


settings = Config()
