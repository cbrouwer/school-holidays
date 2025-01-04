#!/usr/bin/env python3

import asyncio
from datetime import datetime
import requests
import urllib.error

from .const import (
    _LOGGER,
)

class SchoolDaysApi(object):
    API_ENDPOINT_BASE = "https://opendata.rijksoverheid.nl/v1/infotypes/schoolholidays/schoolyear"

    async def call_api(self) -> dict:
        schoolyear = self.get_schoolyear_string()
        api_endpoint = f"{SchoolDaysApi.API_ENDPOINT_BASE}/{schoolyear}?output=json"
        _LOGGER.debug(f"Getting data from: {api_endpoint}")
        try: 
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(None, requests.get, api_endpoint)
            r = await future
            return r.json()['content'][0]['vacations']
        except urllib.error.URLError as exc:
            _LOGGER.error("Error occurred while fetching data: %r", exc)
            return False

    def get_schoolyear_string(self) -> str:
        today = datetime.today().date()
        if (today.month > 8):
            return f"{today.year}-{today.year + 1}"
        return f"{today.year -1 }-{today.year}"