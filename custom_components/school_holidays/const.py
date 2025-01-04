import logging
from datetime import timedelta

DOMAIN = "school_holidays"
CONF_REGION = "region"
MIN_TIME_BETWEEN_UPDATES = timedelta(hours=24, minutes=0)

_LOGGER = logging.getLogger(__name__)