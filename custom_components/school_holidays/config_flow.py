#!/usr/bin/env python3
"""
"""
from typing import Any
from collections.abc import Mapping
import voluptuous as vol

from homeassistant.helpers.selector import (
    SelectSelector,
    SelectOptionDict,
    SelectSelectorConfig,
)
from homeassistant import config_entries

from .const import (
    _LOGGER,
    CONF_REGION,
    DOMAIN,
)

REGION = [
    SelectOptionDict(value="noord", label="Noord"),
    SelectOptionDict(value="midden", label="Midden"),
    SelectOptionDict(value="zuid", label="Zuid"),
]

class SchoolDaysConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_reconfigure(self, user_input: Mapping[str, Any] | None = None):
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry
        if user_input:
            return self.async_update_reload_and_abort(entry, data=user_input, reason="reconfigure_successful")

        return await self._redo_configuration(entry.data)

    async def _redo_configuration(self, entry_data: Mapping[str, Any]):

        schooldays_schema = vol.Schema({
        vol.Required(CONF_REGION): SelectSelector(
                SelectSelectorConfig(options=REGION)
            ),
        })
        return self.async_show_form(step_id="reconfigure", data_schema=schooldays_schema)


    async def async_step_user(self, info):
        if info is not None:
            await self.async_set_unique_id(f"schooldays_{info[CONF_REGION]}")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="SchoolDays for region " + info[CONF_REGION],
                data=info
            )

        schooldays_schema = vol.Schema({
            vol.Required(CONF_REGION): SelectSelector(
                SelectSelectorConfig(options=REGION)
            ),
        })

        return self.async_show_form(
              step_id="user", data_schema=schooldays_schema)



