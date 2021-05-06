from pydantic import BaseSettings


class Config(BaseSettings):
    SLACK_WEBHOOK: str
    MIN_AGE_LIMIT: int = 45
    MIN_AVAILABLE_CAPACITY: int = 1
    POLLING_DELAY_IN_SECONDS: int = 60 * 60
    DYNO_INACTIVITY_DELAY: int = 60 * 25
    CHUNK_SIZE: int = 15
    LOGLEVEL: str = "INFO"
    DATABASE_URL: str

config = Config()
