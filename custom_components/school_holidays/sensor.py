#!/usr/bin/env python3
"""
Sensor component for school-holidays
Author: Chris Brouwer
"""
from __future__ import annotations

from datetime import datetime, date, timedelta
from homeassistant.components.sensor import Entity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import Throttle, dt as dt_util

from .holidays import HolidayRetriever
from .const import (
    _LOGGER,
    MIN_TIME_BETWEEN_UPDATES,
    CONF_REGION,
)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    config = config_entry.data
    region = config.get(CONF_REGION).strip()
    data = SchoolHolidaysData(hass, region)
    await data.async_update()
    async_add_entities([SchoolHolidays(data)])


class SchoolHolidaysData:
    """Fetch and store holiday data for a given region."""

    def __init__(self, hass: HomeAssistant, region: str):
        self.holidays = None
        self.hass = hass
        self.region = region

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        try:
            self.holidays = await HolidayRetriever().get_holidays(self.hass, self.region)
        except Exception as err:
            _LOGGER.error("Error fetching holidays for %s: %s", self.region, err)
            self.holidays = []


class SchoolHolidays(Entity):
    """Representation of a school holiday sensor."""
    _attr_has_entity_name = False

    def __init__(
        self,
        data,
     ) -> None:
        """Initialize the sensor."""
        self._state = None
        self._last_update = None
        self.data = data
        self._attr_name = f"School holidays {data.region.capitalize()}"
        self._attr_unique_id =f"schoolholidays_{data.region}"
        self.friendly_name = f"School holidays for {data.region}"
        self._attr_icon = "mdi:beach"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
    
    def is_weekday(self) -> bool:
        """Return True if today is a weekday."""
        return dt_util.now().weekday() < 5

    async def async_update(self) -> None:
        await self.data.async_update()
        self._last_update = dt_util.now().strftime("%d-%m-%Y %H:%M")
        
        if not self.data.holidays:
            self._state = "unknown"
            return

        
        today = dt_util.now().date()
        is_holiday = any(today >= holiday.start_date  and today < holiday.end_date for holiday in self.data.holidays)
        
        if is_holiday:
            self._state = "holiday"
            self._attr_icon = "mdi:beach"
        elif self.is_weekday():
            self._state = "school day"
            self._attr_icon = "mdi:school"
        else:
            self._state = "weekend"
            self._attr_icon = "mdi:calendar-weekend"
