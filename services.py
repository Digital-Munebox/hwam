"""Services for HWAM integration."""
from __future__ import annotations
import voluptuous as vol
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN, ATTR_START_TIME, ATTR_END_TIME, CONF_DEVICE_ID

TIME_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_ID): str,
    vol.Required(ATTR_START_TIME): cv.time,
    vol.Required(ATTR_END_TIME): cv.time,
})

BASE_SCHEMA = vol.Schema({
    vol.Required(CONF_DEVICE_ID): str,
})

async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up HWAM services."""

    async def set_night_mode_hours(call: ServiceCall) -> None:
        """Set night mode hours."""
        device_id = call.data[CONF_DEVICE_ID]
        start_time = call.data[ATTR_START_TIME]
        end_time = call.data[ATTR_END_TIME]
        
        coordinator = hass.data[DOMAIN][device_id]["coordinator"]
        api = hass.data[DOMAIN][device_id]["api"]
        
        await api.set_night_mode_hours(start_time, end_time)
        await coordinator.async_request_refresh()

    async def enable_night_mode(call: ServiceCall) -> None:
        """Enable night mode."""
        device_id = call.data[CONF_DEVICE_ID]
        coordinator = hass.data[DOMAIN][device_id]["coordinator"]
        api = hass.data[DOMAIN][device_id]["api"]
        
        await api.set_night_mode(True)
        await coordinator.async_request_refresh()

    async def disable_night_mode(call: ServiceCall) -> None:
        """Disable night mode."""
        device_id = call.data[CONF_DEVICE_ID]
        coordinator = hass.data[DOMAIN][device_id]["coordinator"]
        api = hass.data[DOMAIN][device_id]["api"]
        
        await api.set_night_mode(False)
        await coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN, "set_night_mode_hours", set_night_mode_hours, schema=TIME_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "enable_night_mode", enable_night_mode, schema=BASE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, "disable_night_mode", disable_night_mode, schema=BASE_SCHEMA
    )
