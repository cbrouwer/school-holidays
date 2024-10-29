"""Fixtures for testing."""

from unittest.mock import PropertyMock, patch
from pytest_homeassistant_custom_component.common import load_fixture

from custom_components.school_holidays.holidays import Holiday
from datetime import date
import pytest

pytest_plugins = "pytest_homeassistant_custom_component"

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations."""
    return

# This fixture, when used, will have the mocked data 
@pytest.fixture(name="mocked_data")
def mocked_data_fixture(request):
    """Use mocked data in the integration"""
    holidays = [
        Holiday(type="Holiday 1", start_date=date(2024, 1, 10), end_date=date(2024, 1, 15)),
        Holiday(type="Holiday 2", start_date=date(2024, 5, 1), end_date=date(2025, 5, 30)),
    ]
    
    with patch(
        "custom_components.school_holidays.holidays.HolidayRetriever.get_holidays",
        return_value=holidays,
    ):
        yield