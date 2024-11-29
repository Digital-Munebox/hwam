"""The HWAM integration."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import HWAMApi
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]

@callback
def async_setup_services_callback(hass: HomeAssistant) -> None:
    """Set up the HWAM services."""
    async_setup_services(hass)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the HWAM integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HWAM from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = {}
    
    session = async_get_clientsession(hass)
    api = HWAMApi(entry.data[CONF_HOST], session)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=entry.data.get(CONF_NAME, "hwam"),
        update_method=api.async_get_data,
        update_interval=timedelta(
            seconds=entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        ),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    for platform in PLATFORMS:
        if entry.entry_id == list(hass.data[DOMAIN].keys())[0]:
            hass.async_create_task(async_setup_services_callback(hass))
        await hass.config_entries.async_forward_entry_setup(entry, platform)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
