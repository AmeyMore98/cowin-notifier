import urllib.parse


class Constants:
    POLLING_DELAY_IN_SECONDS = 60 * 60
    DYNO_INACTIVITY_DELAY = 60 * 25
    CHUNK_SIZE = 15


class CowinAPIs:
    BASE_URL = "https://cdn-api.co-vin.in"
    CALENDAR_BY_DISTRICT = urllib.parse.urljoin(
        BASE_URL, "/api/v2/appointment/sessions/public/calendarByDistrict"
    )


MARKDOWN = "mrkdwn"
PLAIN_TEXT = "plain_text"
