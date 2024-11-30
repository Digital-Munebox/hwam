"""Support for HWAM fan control."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.fan import (
    FanEntity,
    FanEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the HWAM fan control."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    device_name = entry.data.get("name", "HWAM").lower().replace(" ", "_")

    async_add_entities([HwamFanControl(coordinator, api, device_name)])

class HwamFanControl(CoordinatorEntity, FanEntity):
    """Representation of HWAM fan control."""

    _attr_supported_features = FanEntityFeature.SET_SPEED
    _attr_speed_count = 5

    def __init__(self, coordinator, api, device_name):
        """Initialize the fan control."""
        super().__init__(coordinator)
        self._api = api
        self._attr_name = f"{device_name} burn_level"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_burn_level"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:fire"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": coordinator.config_entry.data.get("name", "HWAM Stove"),
            "manufacturer": "HWAM",
        }

    @property
    def is_on(self) -> bool:
        """Return true if the fan is on."""
        return self.coordinator.data.get("phase") != 5  # 5 = Standby

    @property
    def percentage(self) -> int:
        """Return the current speed percentage."""
        burn_level = self.coordinator.data.get("burn_level", 0)
        return int(burn_level * 20)  # Convert 1-5 to percentage

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan."""
        # Convert percentage to burn level (1-5)
        burn_level = max(1, min(5, int(round(percentage / 20))))
        await self._api.set_burn_level(burn_level)
        await self.coordinator.async_request_refresh()

    async def async_turn_on(self, percentage: int = None, preset_mode: str = None, **kwargs) -> None:
        """Turn on the fan."""
        if not self.is_on:
            await self._api.start()
        if percentage is not None:
            await self.async_set_percentage(percentage)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turning off is not supported - the stove needs to burn out naturally."""
        _LOGGER.warning("Turning off the stove via Home Assistant is not supported for safety reasons.")
