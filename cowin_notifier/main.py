import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from cowin_notifier.api.v1.api import router
from cowin_notifier.api.v1.watch.service import CowinNotifier
from cowin_notifier.decorators import repeat_every
from cowin_notifier.config import config


logging.basicConfig(level=config.LOGLEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cowin-Notifier",
    description="A FastAPI based app to send updates on availability of Covid-19 vaccines",
)

TORTOISE_CONFIG = {
    "connections": {
        "default": config.DB_URL,
    },
    "apps": {
        "models": {
            "models": [
                "cowin_notifier.api.v1.watch.models",
            ],
            "default_connection": "default",
        },
    },
}


# startup tasks
@app.on_event("startup")
async def init_db() -> None:
    """
    Initializes database with Tortoise ORM

    """
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )


@app.on_event("startup")
@repeat_every(seconds=config.POLLING_DELAY_IN_SECONDS, logger=logger, wait_first=True)
async def start_watch_loop() -> None:
    await CowinNotifier().watch_and_notify()


@app.on_event("startup")
@repeat_every(
    seconds=config.DYNO_INACTIVITY_DELAY,
)
def keep_dyno_alive() -> None:
    """Run every 25 minutes to keep Heroku dyno alive"""
    logger.info("We're stayin' alive, stayin' alive Ah, ha, ha, ha, stayin' alive")


@app.get("/ping")
async def ping() -> dict:
    return dict(detail="pong")


app.include_router(router=router, prefix="/api/v1")
