"""Test sensor of SchoolHolidays integration."""


from homeassistant.core import HomeAssistant

from . import setup_component, unload_component


async def test_states(hass: HomeAssistant, mocked_data):
    """Test all sensor states and attributes."""
    config_entry = await setup_component(hass)

    state = hass.states.get("sensor.school_holidays")
    assert state.state == "10.1"

