"""Support for HWAM binary sensors."""
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors for HWAM."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities([
        HWAMBinarySensor(
            coordinator, 
            "door_open", 
            "Porte ouverte",
            BinarySensorDeviceClass.DOOR
        ),
        HWAMBinarySensor(
            coordinator,
            "night_mode",
            "Mode nuit",
            BinarySensorDeviceClass.RUNNING
        ),
    ])

class HWAMBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a HWAM binary sensor."""

    def __init__(self, coordinator, key, name, device_class):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{key}"
        self._attr_device_class = device_class
        self._attr_device_info = {
            "identifiers": {(DOMAIN, coordinator.config_entry.entry_id)},
            "name": coordinator.config_entry.data.get("name", "HWAM Stove"),
            "manufacturer": "HWAM",
        }

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self.coordinator.data.get(self._key, False)
