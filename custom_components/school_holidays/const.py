import logging
from datetime import timedelta

DOMAIN = "school_holidays"

CONF_REGION = "region"
API_BASE_URL = "https://opendata.rijksoverheid.nl/v1/infotypes/schoolholidays/schoolyear/{school_year}?output=json"
GLOBAL_REGION = "heel nederland"

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=24, minutes=0)

_LOGGER = logging.getLogger(__name__)