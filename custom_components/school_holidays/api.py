#!/usr/bin/env python3

import asyncio
import holidays as public_holidays
import requests
import urllib.request
import urllib.error
import json

from .const import (
    _LOGGER,
	API_ENDPOINT,
)

class SchoolDaysApi(object):
	async def call_api(self) -> dict:
		loop = asyncio.get_event_loop()
		future = loop.run_in_executor(None, requests.get, API_ENDPOINT)
		r = await future
		return json.loads(r.text())
		
