import datetime
import logging
import requests
import time
from typing import Union

from fastapi import status

from cowin_notifier.api.v1.watch.constants import Constants, CowinAPIs

logger = logging.getLogger(__name__)


class CowinNotifier:
    @staticmethod
    def get_centers_with_vaccines_in_district(self, district_id: Unions[int, str]):
        all_centers = CowinNotifier.get_all_centers_for_district(district_id)
        return list(filter(CowinNotifier.is_vaccine_available_at_center, all_centers))

    @staticmethod
    def get_all_centers_for_district(district_id: Union[int, str]) -> list:
        params = dict(
            district_id=district_id, date=datetime.datetime.today().strftime("%d-%m-%Y")
        )
        response = requests.get(CowinAPIs.CALENDAR_BY_DISTRICT, params=params)
        if response.status_code != status.HTTP_200_OK:
            logger.error(
                f"CoWin sent non-200 response -> Content: {response.content}, Status Code: {response.status_code}"
            )
            return []
        return response.json().get("centers", [])

    @staticmethod
    def is_vaccine_available_at_center(center_data: list):
        for session in center["sessions"]:
            return session.get("available_capacity", 0) > 1
