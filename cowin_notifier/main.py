import logging

from fastapi import FastAPI

from cowin_notifier.api.v1.api import router
from cowin_notifier.api.v1.watch.service import CowinNotifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Log Watcher")

@app.on_event("startup")
async def start_watch_loop() -> None:
    # TODO: Add code to start loop
    pass

@app.get("/ping")
async def ping() -> dict:
    return dict(detail="pong")


app.include_router(router=router)
