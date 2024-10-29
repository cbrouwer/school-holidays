"""Constants for school holidays tests."""

from homeassistant.const import (
    CONF_REGION,
    CONF_SCAN_INTERVAL,
)

# Mock config data to be used across multiple tests
MOCK_CONFIG = {
    CONF_REGION: "West",
}

MOCK_ENTRY_ID = "test"

MOCK_UPDATE_CONFIG = {CONF_SCAN_INTERVAL: 600}