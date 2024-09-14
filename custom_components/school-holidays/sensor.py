#!/usr/bin/env python3
"""
Sensor component for school-holidays
Author: Chris Brouwer
"""
from __future__ import annotations

from datetime import datetime, date, timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    entities = []
    entities.append(SchoolHolidays())
    async_add_entities(entities, update_before_add=True)



class SchoolHolidays(SensorEntity):
    """Representation of a sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None
        self.entity_id = "sensor.school_holidays"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return 'School holiday'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def is_weekday(self):
        """Check if it is school day."""
        now = datetime.today().weekday() < 5

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = await self.is_weekday()
        self.async_write_ha_state()

    
