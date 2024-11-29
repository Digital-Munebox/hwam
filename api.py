"""HWAM API Client."""
import asyncio
import aiohttp
import async_timeout
import logging
import json
from datetime import time
from typing import Dict, Optional

_LOGGER = logging.getLogger(__name__)

REQUIRED_KEYS = {
    "operation_mode",
    "stove_temperature", 
    "room_temperature",
    "oxygen_level"
}

class HWAMApi:
    def __init__(self, host: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self._host = host
        self._session = session
        self._base_url = f"http://{host}"

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        url = f"{self._base_url}/get_stove_data"
        try:
            async with async_timeout.timeout(15):
                async with self._session.get(url) as response:
                    if response.status == 200:
                        content_type = response.headers.get('Content-Type', '').split(';')[0]
                        if content_type in ['application/json', 'text/json', 'text/plain']:
                            text = await response.text()
                            data = json.loads(text)
                            if all(key in data for key in REQUIRED_KEYS):
                                return data
                    _LOGGER.error("Failed to get data. Status: %s", response.status)
                    return {}
        except Exception as err:
            _LOGGER.error("Error getting data: %s", err)
            raise

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        try:
            data = await self.async_get_data()
            return all(key in data for key in REQUIRED_KEYS)
        except Exception as err:
            _LOGGER.error("Validation failed: %s", err)
            return False

    async def set_night_mode(self, enabled: bool) -> bool:
        """Enable or disable night mode."""
        url = f"{self._base_url}/set_night_mode"
        data = {"enabled": enabled}
        try:
            async with async_timeout.timeout(10):
                async with self._session.post(url, json=data) as response:
                    return response.status == 200
        except Exception as err:
            _LOGGER.error("Error setting night mode: %s", err)
            return False

    async def set_night_mode_hours(self, start_time: time, end_time: time) -> bool:
        """Set night mode hours."""
        url = f"{self._base_url}/set_night_mode_hours"
        data = {
            "start_time": start_time.strftime("%H:%M"),
            "end_time": end_time.strftime("%H:%M")
        }
        try:
            async with async_timeout.timeout(10):
                async with self._session.post(url, json=data) as response:
                    return response.status == 200
        except Exception as err:
            _LOGGER.error("Error setting night mode hours: %s", err)
            return False
