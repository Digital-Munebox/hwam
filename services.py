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

SERVICES = {
    "set_night_mode_hours": {
        "schema": TIME_SCHEMA,
        "handler": "async_set_night_mode_hours"
    },
    "enable_night_mode": {
        "schema": BASE_SCHEMA,
        "handler": "async_enable_night_mode"
    },
    "disable_night_mode": {
        "schema": BASE_SCHEMA,
        "handler": "async_disable_night_mode"
    }
}

async def async_setup_services(hass: HomeAssistant):
    """Set up HWAM services."""
    if hass.data.get(DOMAIN) is None:
        hass.data[DOMAIN] = {}

    async def async_call_service(service_call: ServiceCall):
        """Call correct service based on service_call.service."""
        service = service_call.service
        service_data = service_call.data

        if service in SERVICES:
            device_id = service_data[CONF_DEVICE_ID]
            coordinator = hass.data[DOMAIN][device_id]["coordinator"]
            api = hass.data[DOMAIN][device_id]["api"]

            if service == "set_night_mode_hours":
                await api.set_night_mode_hours(
                    service_data[ATTR_START_TIME],
                    service_data[ATTR_END_TIME]
                )
            elif service == "enable_night_mode":
                await api.set_night_mode(True)
            elif service == "disable_night_mode":
                await api.set_night_mode(False)

            await coordinator.async_request_refresh()

    for service, config in SERVICES.items():
        hass.services.async_register(
            DOMAIN,
            service,
            async_call_service,
            schema=config["schema"]
        )

    return True
