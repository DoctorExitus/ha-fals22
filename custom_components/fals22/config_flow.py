"""Config flow for FALS22 Dewpoint Ventilation integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PASSWORD, default=""): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    session = async_get_clientsession(hass)
    host = data[CONF_HOST]
    password = data.get(CONF_PASSWORD, "")
    name = data.get(CONF_NAME, DEFAULT_NAME)
    
    # Build the test URL
    base_url = f"http://{host}/data/live"
    if password:
        test_url = f"{base_url}?pass={password}"
    else:
        test_url = base_url
    
    try:
        async with async_timeout.timeout(10):
            async with session.get(test_url) as response:
                if response.status != 200:
                    raise CannotConnect(f"HTTP {response.status}")
                
                data_response = await response.json()
                
                # Check for authentication failure
                if isinstance(data_response, dict) and data_response.get("auth") is False:
                    raise InvalidAuth("Authentication failed")
                
                # Validate response structure
                if isinstance(data_response, list) and data_response:
                    data_response = data_response[0]
                
                if not isinstance(data_response, dict):
                    raise InvalidData("Invalid response format")
                
                # Check for expected fields
                required_fields = ["temp_in", "temp_out", "hum_in", "hum_out"]
                if not all(field in data_response for field in required_fields):
                    raise InvalidData("Missing required data fields")
                    
    except asyncio.TimeoutError as err:
        raise CannotConnect("Connection timeout") from err
    except aiohttp.ClientError as err:
        raise CannotConnect(f"Connection error: {err}") from err

    # Return info that you want to store in the config entry.
    return {
        "title": f"{name} ({host})",
        "host": host,
        "name": name,
        "password": password,
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for FALS22 Dewpoint Ventilation."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except InvalidData:
                errors["base"] = "invalid_data"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Check if already configured using host as unique_id
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for FALS22."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema(
            {
                vol.Optional(
                    "scan_interval",
                    default=self.config_entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=30, max=3600)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class InvalidData(HomeAssistantError):
    """Error to indicate there is invalid data."""
