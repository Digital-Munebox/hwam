"""Services for HWAM integration."""
from homeassistant.core import HomeAssistant, ServiceCall
import voluptuous as vol
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

async def handle_set_night_mode_hours(hass: HomeAssistant, service_call: ServiceCall):
    """Handle set_night_mode_hours service."""
    device_id = service_call.data[CONF_DEVICE_ID]
    coordinator = hass.data[DOMAIN][device_id]["coordinator"]
    api = hass.data[DOMAIN][device_id]["api"]
    
    await api.set_night_mode_hours(
        service_call.data[ATTR_START_TIME],
        service_call.data[ATTR_END_TIME]
    )
    await coordinator.async_request_refresh()

async def handle_enable_night_mode(hass: HomeAssistant, service_call: ServiceCall):
    """Handle enable_night_mode service."""
    device_id = service_call.data[CONF_DEVICE_ID]
    coordinator = hass.data[DOMAIN][device_id]["coordinator"]
    api = hass.data[DOMAIN][device_id]["api"]
    
    await api.set_night_mode(True)
    await coordinator.async_request_refresh()

async def handle_disable_night_mode(hass: HomeAssistant, service_call: ServiceCall):
    """Handle disable_night_mode service."""
    device_id = service_call.data[CONF_DEVICE_ID]
    coordinator = hass.data[DOMAIN][device_id]["coordinator"]
    api = hass.data[DOMAIN][device_id]["api"]
    
    await api.set_night_mode(False)
    await coordinator.async_request_refresh()

async def async_setup_services(hass: HomeAssistant) -> bool:
    """Set up HWAM services."""
    if not hass.data.get(DOMAIN):
        hass.data[DOMAIN] = {}

    if not hass.services.has_service(DOMAIN, "set_night_mode_hours"):
        hass.services.async_register(
            DOMAIN,
            "set_night_mode_hours",
            handle_set_night_mode_hours,
            schema=TIME_SCHEMA,
        )

    if not hass.services.has_service(DOMAIN, "enable_night_mode"):
        hass.services.async_register(
            DOMAIN,
            "enable_night_mode",
            handle_enable_night_mode,
            schema=BASE_SCHEMA,
        )

    if not hass.services.has_service(DOMAIN, "disable_night_mode"):
        hass.services.async_register(
            DOMAIN,
            "disable_night_mode",
            handle_disable_night_mode,
            schema=BASE_SCHEMA,
        )

    return True
