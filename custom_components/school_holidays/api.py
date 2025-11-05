#!/usr/bin/env python3

import asyncio
import holidays as public_holidays
import requests
import urllib.request
import urllib.error

from .const import _LOGGER
from .utils import get_school_year_endpoints

class SchoolDaysApi(object):
    async def call_api(self) -> list:
        """
        Fetch school holiday data from the API.
        May query multiple school years if we're in August/September to catch
        summer holidays that extend into the new school year.

        Returns:
            list: Combined list of vacation data from all queried school years
        """
        endpoints = get_school_year_endpoints()
        all_vacations = []

        for endpoint in endpoints:
            try:
                _LOGGER.info(f"Fetching school holidays from: {endpoint}")
                loop = asyncio.get_event_loop()
                future = loop.run_in_executor(None, requests.get, endpoint)
                r = await future
                vacations = r.json()['content'][0]['vacations']
                all_vacations.extend(vacations)
            except urllib.error.URLError as exc:
                _LOGGER.error("Error occurred while fetching data from %s: %r", endpoint, exc)
            except (KeyError, IndexError) as exc:
                _LOGGER.error("Error parsing response from %s: %r", endpoint, exc)

        if not all_vacations:
            return False

        return all_vacations
