"""Support for HWAM start button."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
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
    """Set up HWAM button based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    device_name = entry.data.get("name", "HWAM").lower().replace(" ", "_")

    async_add_entities([HwamStartButton(coordinator, api, device_name)])

class HwamStartButton(CoordinatorEntity, ButtonEntity):
    """Representation of HWAM start button."""

    def __init__(self, coordinator, api, device_name):
        """Initialize the button."""
        super().__init__(coordinator)
        self._api = api
        self._attr_name = f"{device_name} start"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_start"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:power"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": coordinator.config_entry.data.get("name", "HWAM Stove"),
            "manufacturer": "HWAM",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._api.start()
        await self.coordinator.async_request_refresh()
