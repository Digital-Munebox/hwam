"""Support for HWAM burn level control."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

BURN_LEVELS = ["1", "2", "3", "4", "5"]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigType,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the HWAM burn level control."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    device_name = entry.data.get("name", "HWAM").lower().replace(" ", "_")

    async_add_entities([HwamBurnLevelControl(coordinator, api, device_name)])

class HwamBurnLevelControl(CoordinatorEntity, SelectEntity):
    """Representation of HWAM burn level control."""

    def __init__(self, coordinator, api, device_name):
        """Initialize the burn level control."""
        super().__init__(coordinator)
        self._api = api
        self._attr_name = f"{device_name} niveau_de_combustion"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_burn_level"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:fire"
        self._attr_options = BURN_LEVELS
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": coordinator.config_entry.data.get("name", "HWAM Stove"),
            "manufacturer": "HWAM",
        }

    @property
    def current_option(self) -> str | None:
        """Return the current burn level."""
        burn_level = self.coordinator.data.get("burn_level")
        if burn_level is None:
            return None
        return str(burn_level)

    async def async_select_option(self, option: str) -> None:
        """Change the burn level."""
        await self._api.set_burn_level(int(option))
        await self.coordinator.async_request_refresh()
