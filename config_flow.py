"""Config flow for HWAM integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_SCAN_INTERVAL
import logging
from .api import HWAMApi
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
    vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
})

class HWAMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HWAM."""
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            session = self.hass.helpers.aiohttp_client.async_get_clientsession()
            api = HWAMApi(user_input[CONF_HOST], session)

            try:
                if await api.async_validate_connection():
                    await api.close()
                    return self.async_create_entry(
                        title=user_input[CONF_NAME],
                        data=user_input
                    )
                errors["base"] = "cannot_connect"
            except asyncio.TimeoutError:
                errors["base"] = "timeout"
            except Exception:
                _LOGGER.exception("Unexpected error")
                errors["base"] = "unknown"
            finally:
                await api.close()

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors
        )
