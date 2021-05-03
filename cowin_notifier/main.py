import logging

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from cowin_notifier.api.v1.api import router
from cowin_notifier.api.v1.watch.service import CowinNotifier
from cowin_notifier.api.v1.watch.constants import Constants
from cowin_notifier.api.v1.watch.models import District

district = District()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CoWin-Notifier")


@app.on_event("startup")
@repeat_every(seconds=Constants.WAIT_TIME_IN_SECONDS, wait_first=True)
def start_watch_loop() -> None:
    centers = CowinNotifier.get_centers_in_district_with_vaccines(district_id=district.id)
    message = ""
    for center in centers:
        message += f"Pincode: {center.get('pincode')}\n"
        message += f"Centre Name: {center.get('name')}\n"
        message += f"From: {center.get('from')}\n"
        message += f"To: {center.get('to')}\n\n"

        for index, session in enumerate(center.get("sessions", [])):
            if index == 0:
                message += f"Sessions/ Slots: \n"
            message += f"Available Capacity: {session.get('available_capacity')}\n"
            message += f"Vaccine: {session.get('vaccine')}\n"
            message += f"Slots Available In: {', '.join(session.get('slots'))}\n"
    logger.info(f"Message: {message}")


@app.get("/ping")
async def ping() -> dict:
    return dict(detail="pong")


app.include_router(router=router)
