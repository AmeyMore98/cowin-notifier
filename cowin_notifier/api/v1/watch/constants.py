import urllib.parse


class CowinAPIs:
    BASE_URL = "https://cdn-api.co-vin.in"
    CALENDAR_BY_DISTRICT = urllib.parse.urljoin(
        BASE_URL, "/api/v2/appointment/sessions/public/calendarByDistrict"
    )


MARKDOWN = "mrkdwn"
PLAIN_TEXT = "plain_text"
