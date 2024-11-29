"""Support for HWAM binary sensors."""
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

BINARY_SENSORS = [
    {
        "key": "door_open",
        "name": "Porte ouverte",
        "device_class": BinarySensorDeviceClass.DOOR,
        "icon": "mdi:door",
    },
    {
        "key": "night_mode",
        "name": "Mode nuit",
        "device_class": BinarySensorDeviceClass.RUNNING,
        "icon": "mdi:weather-night",
    },
]

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors for HWAM."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities([
        HWAMBinarySensor(coordinator, sensor["key"], sensor["name"], sensor["device_class"], sensor.get("icon"))
        for sensor in BINARY_SENSORS
    ])

class HWAMBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a HWAM binary sensor."""

    def __init__(self, coordinator, key, name, device_class, icon=None):
        """Initialize the binary sensor."""
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
        if icon:
            self._attr_icon = icon

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        value = self.coordinator.data.get(self._key)
        # Conversion des valeurs possibles en booléen
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.lower() in ("true", "1", "on", "yes")
        return False
