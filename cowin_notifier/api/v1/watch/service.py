import datetime
import logging
from typing import Any, List

import requests

from cowin_notifier.api.v1.watch.constants import MARKDOWN, PLAIN_TEXT, CowinAPIs, Constants
from cowin_notifier.api.v1.watch.models import District
from cowin_notifier.config import config
from cowin_notifier.utils import SlackFormater, requests_retry_session, slack_alert, chunks

logger = logging.getLogger(__name__)


class CowinNotifier:
    """
    Class to monitor and notify vaccine availability
    """

    def __init__(self) -> None:
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

        if response.status_code != 200:
            logging.error(f"Cowin returned non-200 response -> Code: {response.status_code}, Content: {response.content}")
            return []

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
        # todo: change these coditions as required
        for session in center["sessions"]:
            return (
                session.get("available_capacity", 0) > config.MIN_AVAILABLE_CAPACITY
                and session.get("min_age_limit", 0) <= config.MIN_AGE_LIMIT
            )

    def notify_slack(self, district_centers: List[dict]) -> None:
        """
        Format Slack specific message and send over webhook
        # Todo: Send messages in batch

        Args:
            district_centers (List[dict]): district wise vaccine data
        """
        for district_center in district_centers:
            for centers in chunks(district_center.get("centers", []), Constants.CHUNK_SIZE):
                slack_formatter = SlackFormater()
                # there will always be at least one center for each district
                state = centers[0].get("state_name")
                district = centers[0].get("district_name")

                # header of statea and district
                slack_formatter.add_header(f"{district}, {state} :zap:", PLAIN_TEXT)
                slack_formatter.add_divider()

                # centers signify all the vaccine centers available in the district
                for itr, center in enumerate(centers):
                    cb_options = []
                    # sessions signify the dates available for each center
                    for center_date in center.get("sessions", []):
                        available_date = center_date.get("date")

                        option_description = (
                            f"  |  *Available Capacity*: {center_date.get('available_capacity')}"
                            f"  |  *Min Age*: {center_date.get('min_age_limit')}"
                            f"  |  :syringe: {center_date.get('vaccine', 'NA')}"
                        )
                        cb_text = f"{available_date}{option_description}"
                        cb_option = slack_formatter.get_checkbox_option(
                            cb_text,
                            MARKDOWN,
                            available_date,
                        )
                        cb_options.append(cb_option)

                    checkbox = slack_formatter.get_checkbox(cb_options, f"cb-{itr}")
                    center_name, center_pincode = (
                        center.get("name"),
                        center.get("pincode"),
                    )
                    center_details = f"*{center_name}* \t   *PIN* {center_pincode}"
                    slack_formatter.add_section(center_details, MARKDOWN, checkbox)

                    slack_formatter.add_divider()

                # notify over slack webhook for each district
                payload = slack_formatter.get_blocks()
                if payload.get("blocks"):
                    slack_alert(
                        config.SLACK_WEBHOOK,
                        payload,
                    )

    def notify(self, district_centers: List[dict]) -> Any:
        """
        Notify vaccine availability over desired medium

        Args:
            district_centers (List[dict]): district wise vaccine data

        Returns:
            Any: notify response
        """
        return self.notify_slack(district_centers)

    async def watch_and_notify(self) -> Any:
        """
        Monitor Cowin APIs and notify when vaccines are available

        Returns:
            Any: notify response
        """
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
