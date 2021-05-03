from typing import Iterable

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


async def slack_alert(endpoint: str, msg: str):
    payload = {
        "text": str(msg),
        "username": "GlamAR-Bot",
        "icon_emoji": ":glamar-logo:",
    }
    requests.post(url=endpoint, json=payload)
