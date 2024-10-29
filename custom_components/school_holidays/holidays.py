#!/usr/bin/env python3

import holidays as public_holidays
import json
from datetime import datetime, date
from dataclasses import dataclass

from .api import SchoolDaysApi

from .const import (
    _LOGGER,
	GLOBAL_REGION
)

@dataclass
class Holiday:
    type: str
    start_date: date
    end_date: date

class HolidayRetriever(object):
	async def get_holidays(self, region) -> list[Holiday]:
		schoolHolidays = await self.get_school_holidays(region)
		publicHolidays = await self.get_public_holidays()
		return schoolHolidays + publicHolidays
		
	async def get_school_holidays(self, region):
		_LOGGER.info(f"Retrieving national school holidays for {region}")
		
		try:
			apiData = await SchoolDaysApi().call_api()
			holidays = []
			for vacation in apiData['content'][0]['vacations']:
				vacation_type = vacation['type'].strip()
				start_date, end_date = self.get_dates_for_region(vacation, region)
				if start_date and end_date:
					_LOGGER.debug(f"Found a holiday: {vacation_type} from {start_date} to {end_date}.")
					start_date = datetime.fromisoformat(start_date[:-1]).date()
					end_date = datetime.fromisoformat(end_date[:-1]).date()
					holidays.append(Holiday(vacation_type, start_date, end_date))
			_LOGGER.info(f"Found {len(holidays)} holidays")
			return holidays
		except urllib.error.URLError as exc:
			_LOGGER.error("Error occurred while fetching data: %r", exc.reason)
			return False
		except Exception as exc:
			_LOGGER.error(
                f"""Error occurred! {exc}""", exc
            )
			return False
	

	async def get_public_holidays(self) -> list[Holiday]:
		_LOGGER.info(f"Retrieving public holidays")
		holidays = []
		for date, name in public_holidays.NL(years=2024).items():
			_LOGGER.info(f"Found public holiday: {name} {date}")
			holidays.append(Holiday(name, date, date))
		return holidays
			
		
	def get_dates_for_region(self, data, region) -> tuple[date, date]:
		# Try to find preferred region first, then fallback to GLOBAL_REGION
		region_priority = [region, GLOBAL_REGION]
		return next(
			((region['startdate'], region['enddate']) for region in data['regions']
			if region['region'].strip().lower() in region_priority),
			(None, None)  # Fallback if neither is found
		)

		
