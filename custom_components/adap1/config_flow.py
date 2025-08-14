import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

class AdaOkosMeroConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ADA Okos mérő."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            existing_names = [entry.title for entry in self._async_current_entries()]
            if user_input["friendly_name"] in existing_names:
                errors["friendly_name"] = "name_exists"
            else:
                return self.async_create_entry(title=user_input["friendly_name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("friendly_name"): str,
                vol.Required("host", default=DEFAULT_HOST): str,
                vol.Required("port", default=DEFAULT_PORT): int,
                vol.Required("update_interval", default=DEFAULT_UPDATE_INTERVAL): int,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return AdaOkosMeroOptionsFlow(config_entry)

class AdaOkosMeroOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for ADA Okos mérő."""

    def __init__(self, config_entry):
        self._data = config_entry.data

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("host", default=self._data.get("host")): str,
                vol.Required("port", default=self._data.get("port")): int,
                vol.Required("update_interval", default=self._data.get("update_interval")): int,
            }),
        )
