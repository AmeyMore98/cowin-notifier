from pydantic import BaseSettings


class Config(BaseSettings):
    SLACK_WEBHOOK: str
    MIN_AGE_LIMIT: int = 45

config = Config()
