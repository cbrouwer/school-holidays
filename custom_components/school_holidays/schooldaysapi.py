#!/usr/bin/env python3

import asyncio
import holidays as public_holidays
import requests
import urllib.request
import urllib.error
from datetime import datetime, date
from dataclasses import dataclass

from .const import (
    _LOGGER,
	API_ENDPOINT,
	GLOBAL_REGION
)

class SchoolDaysApi(object):

	async def get_holidays(self, region):
		schoolHolidays = await self.get_school_holidays(region)
		publicHolidays = await self.get_public_holidays()
		return schoolHolidays + publicHolidays
		
	async def get_school_holidays(self, region):
		_LOGGER.info(f"Retrieving national school holidays for {region}")
		
		try:
			holidays = []
			loop = asyncio.get_event_loop()
			future = loop.run_in_executor(None, requests.get, API_ENDPOINT)
			r = await future

            # r = await requests.get(url=API_ENDPOINT, timeout=10)
			rawData = r.json()
			for vacation in rawData['content'][0]['vacations']:
				vacation_type = vacation['type'].strip()
        
				start_date, end_date = self.get_dates_for_region(vacation, region)
				if start_date and end_date:
					_LOGGER.debug(f"Found a holiday: {vacation_type} from {start_date} to {end_date}.")
					start_date = datetime.fromisoformat(start_date[:-1]).date()
					end_date = datetime.fromisoformat(end_date[:-1]).date()
					holidays.append(Holiday(vacation_type, start_date, end_date))

			return holidays
		except urllib.error.URLError as exc:
			_LOGGER.error("Error occurred while fetching data: %r", exc.reason)
			return False
		except Exception as exc:
			_LOGGER.error(
                f"""Error occurred! {exc}"""
            )
			return False
		
	async def get_public_holidays(self): 
		_LOGGER.info(f"Retrieving public holidays")
		holidays = []
		_LOGGER.info(f"Got holidays: {public_holidays.NL(years=2024)}")
		for date, name in public_holidays.NL(years=2024).items():
			_LOGGER.info(f"Found public holiday: {name} {date}")
			holidays.append(Holiday(name, date, date))
		return holidays
			
		
	def get_dates_for_region(self, data, region):
		# Try to find preferred region first, then fallback to GLOBAL_REGION
		region_priority = [region, GLOBAL_REGION]
		return next(
			((region['startdate'], region['enddate']) for region in data['regions']
			if region['region'].strip().lower() in region_priority),
			(None, None)  # Fallback if neither is found
		)

		

    
@dataclass
class Holiday:
    type: str
    start_date: date
    end_date: date