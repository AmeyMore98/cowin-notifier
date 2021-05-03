import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from cowin_notifier.api.v1.api import router

# from fastapi_utils.tasks import repeat_every
from cowin_notifier.decorators import repeat_every

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cowin-Notifier")

TORTOISE_CONFIG = {
    "connections": {
        "default": "sqlite://db.sqlite3",
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


# @app.on_event("startup")
# @repeat_every(seconds=1)  # 1 hour
# async def start_watch_loop() -> None:
#     import time
#     print(f"Recurring task executed at: {time.time()}")


@app.get("/ping")
async def ping() -> dict:
    return dict(detail="pong")


app.include_router(router=router)
