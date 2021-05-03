import datetime
import logging
from typing import List

import requests

from cowin_notifier.api.v1.watch.constants import CowinAPIs
from cowin_notifier.api.v1.watch.models import District
from cowin_notifier.utils import requests_retry_session

district = District()

logger = logging.getLogger(__name__)


class CowinNotifier:
    def __init__(self):
        self.date = datetime.datetime.today().strftime("%d-%m-%Y")

    def watch(self, district_id: int) -> List[dict]:
        """
        Hit Cowin district API
        Discard centers with
            - available_capacity < 1
            - min_age_limit >= 45

        Args:
            district_id (int): district_id

        Returns:
            List[dict]: [description]
        """
        session = requests.Session()
        session.params = dict(district_id=district_id, date=self.date)
        response = requests_retry_session(session=session).get(
            CowinAPIs.CALENDAR_BY_DISTRICT
        )

        response_data = response.json()
        return list(
            filter(
                CowinNotifier.filter_center_by_availability_and_age,
                response_data.get("centers", []),
            )
        )

    @staticmethod
    def filter_center_by_availability_and_age(center: list):
        """
        Filter by availability and age
        - `available_capacity` greater than 0
        - `min_age_limit` lesser than 45

        Args:
            center (list): center details
        """
        for session in center["sessions"]:
            return (
                session.get("available_capacity", 0) > 1
                and session.get("min_age_limit", 0) <= 45
            )

    def notify(self, district_centers: List[dict]):
        pretty_data = []
        for district_center in district_centers:
            # there will always be at least one center for each district
            state_data = dict(
                state=district_center.get("centers")[0].get("state_name"), centers=[]
            )
            for center in district_center.get("centers", []):
                state_data["centers"].append(
                    dict(
                        state_name=center.get("state_name"),
                        district_name=center.get("district_name"),
                        center_name=center.get("name"),
                        pincode=center.get("pincode"),
                        fee_type=center.get("fee_type"),
                        dates=center.get("sessions"),
                    )
                )
            pretty_data.append(state_data)
        return pretty_data

    async def watch_and_notify(self) -> None:
        districts = await District.all().order_by("id")
        district_centers = []
        for district in districts:
            centers = self.watch(district.id)
            if centers:
                district_centers.append(
                    dict(
                        district_id=district.id,
                        district_name=district.name,
                        centers=centers,
                    )
                )
        return self.notify(district_centers)
