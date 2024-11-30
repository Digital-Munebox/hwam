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
    "oxygen_level",
    "burn_level",
    "phase"
}

class HWAMApi:
    def __init__(self, host: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self._host = host
        self._session = session
        self._base_url = f"http://{host}"
        self._retry_count = 3
        self._retry_delay = 2

    async def _api_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make an API request with retry mechanism."""
        url = f"{self._base_url}{endpoint}"
        for attempt in range(self._retry_count):
            try:
                async with async_timeout.timeout(15):
                    if method.upper() == "GET":
                        async with self._session.get(url) as response:
                            if response.status == 200:
                                return await self._process_response(response)
                    else:  # POST
                        async with self._session.post(url, json=data) as response:
                            if response.status == 200:
                                return await self._process_response(response)
                    
                    _LOGGER.error("Request failed with status: %s", response.status)
            except asyncio.TimeoutError:
                _LOGGER.warning("Timeout on attempt %d of %d", attempt + 1, self._retry_count)
            except Exception as err:
                _LOGGER.error("Error on attempt %d of %d: %s", attempt + 1, self._retry_count, err)
            
            if attempt < self._retry_count - 1:
                await asyncio.sleep(self._retry_delay)
        
        raise Exception(f"Failed to communicate with HWAM stove after {self._retry_count} attempts")

    async def _process_response(self, response) -> Dict:
        """Process API response."""
        try:
            text = await response.text()
            data = json.loads(text)
            return data
        except json.JSONDecodeError as err:
            raise ValueError(f"Invalid JSON response: {err}")

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        try:
            data = await self._api_request("GET", "/get_stove_data")
            if all(key in data for key in REQUIRED_KEYS):
                return data
            missing_keys = REQUIRED_KEYS - set(data.keys())
            _LOGGER.error("Missing required keys in response: %s", missing_keys)
            return {}
        except Exception as err:
            _LOGGER.error("Error getting data: %s", err)
            raise

    async def set_burn_level(self, level: int) -> bool:
        """Set the burn level (1-5)."""
        if not 1 <= level <= 5:
            raise ValueError("Burn level must be between 1 and 5")
        
        try:
            data = {"level": level}
            response = await self._api_request("POST", "/set_burn_level", data)
            return response.get("response") == "OK"
        except Exception as err:
            _LOGGER.error("Error setting burn level: %s", err)
            return False

    async def start(self) -> bool:
        """Start the stove."""
        try:
            response = await self._api_request("GET", "/start")
            return response.get("response") == "OK"
        except Exception as err:
            _LOGGER.error("Error starting stove: %s", err)
            return False

    # [Les autres méthodes existantes restent inchangées...]
