from pydantic import BaseSettings


class Config(BaseSettings):
    SLACK_WEBHOOK: str
    MIN_AGE_LIMIT: int = 45
    MIN_AVAILABLE_CAPACITY: int = 1

config = Config()
