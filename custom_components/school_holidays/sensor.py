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
from homeassistant.util import Throttle

from .schooldaysapi import SchoolDaysApi
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

    data = SchoolHolidaysData(region)
    await data.async_update()

    entities = []
    entities.append(SchoolHolidays(data))

    async_add_entities(entities)


class SchoolHolidaysData(object):
    def __init__(self, region):
        self.data = None
        self.region = region

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        self.data = await SchoolDaysApi().get_holidays(self.region)



class SchoolHolidays(Entity):
    """Representation of a sensor."""
    _attr_has_entity_name = True

    def __init__(
        self,
        data,
     ) -> None:
        """Initialize the sensor."""
        self._state = None
        self.entity_id = "sensor.school_holidays"
        self.data = data
        self.friendly_name = 'School holiday'
        self._state = None
        self._last_update = None

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'School holiday'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def is_weekday(self):
        """Check if it is school day."""
        now = datetime.today().weekday() < 5

    @Throttle(timedelta(minutes=1))
    async def async_update(self) -> None:
        await self.data.async_update()
        self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
        
        if (self.data.data):
            today = datetime.today().date()
            _LOGGER.debug("Checking for holidays for %s in %s", str(today), str(self.data.data))
            self._state = any(today >= holiday.start_date  and today < holiday.end_date for holiday in self.data.data)


