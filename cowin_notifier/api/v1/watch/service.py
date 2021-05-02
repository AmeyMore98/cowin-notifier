import datetime
import logging
import requests
import time

from fastapi import status

from cowin_notifier.api.v1.watch.constants import Constants, CowinAPIs
from cowin_notifier.api.v1.watch.models import District

district = District()

logger = logging.getLogger(__name__)


class CowinNotifier:
    async def watch_and_notify(self):
        params = dict(
            district_id=district.id, date=datetime.datetime.today().strftime("%d-%m-%Y")
        )
        response = requests.get(CowinAPIs.CALENDAR_BY_DISTRICT, params=params)
        if response.status_code != status.HTTP_200_OK:
            logger.error(
                f"CoWin sent non-200 response -> Content: {response.content}, Status Code: {response.status_code}"
            )
            return
        response_data = response.json()
        filtered_centers = list(
            filter(
                CowinNotifier.filter_center_by_availability,
                response_data.get("centers", []),
            )
        )
        if filtered_centers == []:
            return
        return filtered_centers

    @staticmethod
    def filter_center_by_availability(center: list):
        for session in center["sessions"]:
            return session.get("available_capacity", 0) > 1
