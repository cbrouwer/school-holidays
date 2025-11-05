#!/usr/bin/env python3

from datetime import date
from .const import API_BASE_URL


def get_current_school_year() -> tuple[int, int]:
    """
    Get the current school year range.
    A school year runs from August 1 of year X to July 31 of year X+1.

    Returns:
        tuple[int, int]: (start_year, end_year) of the school year
    """
    today = date.today()
    if today.month >= 8:  # August or later
        return (today.year, today.year + 1)
    else:  # Before August
        return (today.year - 1, today.year)


def should_query_previous_school_year() -> bool:
    """
    Determine if we should also query the previous school year.
    This is needed in August/September to catch summer holidays that extend
    into the new school year but are only present in the previous year's data.

    Returns:
        bool: True if we should query the previous school year
    """
    today = date.today()
    return today.month in [8, 9]  # August or September


def get_api_endpoint(start_year: int, end_year: int) -> str:
    """
    Build the API endpoint URL for a specific school year.

    Args:
        start_year: Starting year of the school year
        end_year: Ending year of the school year

    Returns:
        str: Complete API endpoint URL
    """
    school_year = f"{start_year}-{end_year}"
    return API_BASE_URL.format(school_year=school_year)


def get_school_year_endpoints() -> list[str]:
    """
    Get the API endpoint(s) to query for school holidays.
    Returns multiple endpoints when we're in August/September to catch
    summer holidays that might extend into the new school year.

    Returns:
        list[str]: List of API endpoint URLs to query
    """
    current_start, current_end = get_current_school_year()
    endpoints = [get_api_endpoint(current_start, current_end)]

    if should_query_previous_school_year():
        # Also query previous school year
        prev_start = current_start - 1
        prev_end = current_end - 1
        endpoints.append(get_api_endpoint(prev_start, prev_end))

    return endpoints
