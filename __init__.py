"""The FALS22 Dewpoint Ventilation integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up FALS22 from a config entry."""
    coordinator = FALS22DataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class FALS22DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the FALS22 API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.hass = hass
        self.entry = entry
        self.host = entry.data["host"]
        self.password = entry.data.get("password")
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    def _get_url(self, endpoint: str) -> str:
        """Get the full URL for an endpoint."""
        base_url = f"http://{self.host}"
        if self.password:
            return f"{base_url}{endpoint}?pass={self.password}"
        return f"{base_url}{endpoint}"

    async def _async_fetch_data(self, endpoint: str) -> dict | list:
        """Fetch data from a specific endpoint."""
        url = self._get_url(endpoint)
        try:
            async with async_timeout.timeout(10):
                async with self.session.get(url) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: {response.status}")
                    
                    data = await response.json()
                    
                    # Check for authentication failure
                    if isinstance(data, dict) and data.get("auth") is False:
                        raise UpdateFailed("Authentication failed")
                    
                    return data
        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout fetching data") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

    async def _async_update_data(self) -> dict:
        """Update data via library."""
        try:
            # Fetch live data
            live_data = await self._async_fetch_data("/data/live")
            settings_data = await self._async_fetch_data("/data/settings")
            
            # Extract single objects from arrays if needed
            if isinstance(live_data, list) and live_data:
                live_data = live_data[0]
            if isinstance(settings_data, list) and settings_data:
                settings_data = settings_data[0]
            
            return {
                "live": live_data,
                "settings": settings_data,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    async def async_set_manual_mode(self, duration: int, turn_on: bool) -> bool:
        """Set manual ventilation mode."""
        url = self._get_url("/postmanually")
        data = {
            "duration": duration,
            "on": 1 if turn_on else 0,
        }
        
        try:
            async with async_timeout.timeout(10):
                async with self.session.post(url, data=data) as response:
                    return response.status == 200
        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            _LOGGER.error("Error setting manual mode: %s", err)
            return False

    async def async_update_settings(self, settings: dict) -> bool:
        """Update device settings."""
        url = self._get_url("/postsettings")
        
        try:
            async with async_timeout.timeout(10):
                async with self.session.post(url, data=settings) as response:
                    return response.status == 200
        except (asyncio.TimeoutError, aiohttp.ClientError) as err:
            _LOGGER.error("Error updating settings: %s", err)
            return False