import json
from typing import Iterable, List

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def requests_retry_session(
    retries: int = 5,
    backoff_factor: float = 0.3,
    status_forcelist: Iterable = (500, 502, 504),
    session: requests.Session = None,
) -> requests.Session:
    """
    Hits an Endpoint with retries

    Args:
        retries (int, optional): Retry count. Defaults to 5.
        backoff_factor (float, optional): exponential delay factor after every retry. Defaults to 0.3.
        status_forcelist (Iterable, optional): HTTP status codes to force a retry on. Defaults to (500, 502, 504).
        session (requests.Session, optional): Requests session. Defaults to None.

    Returns:
        Session: Requests Session

    Ref: https://www.peterbe.com/plog/best-practice-with-retries-with-requests
         https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def slack_alert(endpoint: str, payload: dict) -> requests.Response:
    """
    Send message to Slack webhook
    # todo: make use of requests_retry_session()
    Args:
        endpoint (str): URL to hit
        payload (dict): payload

    Returns:
        requests.Response: Response object
    """
    return requests.post(url=endpoint, data=json.dumps(payload))


class SlackFormater:
    """
    Class to encapsulate Slack Block Kit formatting
    """

    def __init__(self) -> None:
        self.blocks: List[dict] = []

    def add_divider(self) -> None:
        self.blocks.append(dict(type="divider"))

    def _text_type(self, text: str, text_type: str) -> dict:
        return dict(type=text_type, text=text)

    def add_header(self, text: str, text_type: str) -> None:
        self.blocks.append(
            dict(
                type="header",
                text=dict(
                    type=text_type,
                    text=text,
                    emoji=True,
                ),
            )
        )

    def add_section(self, text: str, text_type: str, accessory: dict = {}) -> None:
        self.blocks.append(
            dict(
                type="section",
                text=self._text_type(
                    text,
                    text_type,
                ),
                accessory=accessory,
            )
        )

    def get_checkbox_option(
        self,
        text: str,
        text_type: str,
        value: str,
    ) -> dict:
        return dict(
            text=self._text_type(
                text,
                text_type,
            ),
            value=value,
        )

    def get_checkbox(self, options: List[dict], action_id: str) -> dict:
        return dict(type="checkboxes", options=options, action_id=action_id)

    def get_blocks(self) -> dict:
        return dict(blocks=self.blocks)
