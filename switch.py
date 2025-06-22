"""Support for FALS22 switches."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER, MODEL, SWITCH_TYPES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FALS22 switches from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    switches = [
        FALS22ManualModeSwitch(coordinator, config_entry),
        FALS22KeylockSwitch(coordinator, config_entry),
    ]

    async_add_entities(switches)


class FALS22ManualModeSwitch(CoordinatorEntity, SwitchEntity):
    """Switch to control manual ventilation mode."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, config_entry: ConfigEntry) -> None:
        """Initialize the manual mode switch."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_manual_mode"
        self._attr_translation_key = SWITCH_TYPES["manual_mode"]["translation_key"]
        self._attr_icon = SWITCH_TYPES["manual_mode"]["icon"]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.entry_id)},
            name="FALS22 Dewpoint Ventilation",
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="6.0+",
            configuration_url=f"http://{self._config_entry.data['host']}",
        )

    @property
    def is_on(self) -> bool:
        """Return true if manual mode is on."""
        live_data = self.coordinator.data.get("live", {})
        return live_data.get("on", 0) == 1

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on manual ventilation for 30 minutes."""
        success = await self.coordinator.async_set_manual_mode(30, True)
        if success:
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off manual ventilation for 30 minutes."""
        success = await self.coordinator.async_set_manual_mode(30, False)
        if success:
            await self.coordinator.async_request_refresh()


class FALS22KeylockSwitch(CoordinatorEntity, SwitchEntity):
    """Switch to control device keylock."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, config_entry: ConfigEntry) -> None:
        """Initialize the keylock switch."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_keylock"
        self._attr_translation_key = SWITCH_TYPES["keylock"]["translation_key"]
        self._attr_icon = SWITCH_TYPES["keylock"]["icon"]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.entry_id)},
            name="FALS22 Dewpoint Ventilation",
            manufacturer=MANUFACTURER,
            model=MODEL,
            sw_version="6.0+",
            configuration_url=f"http://{self._config_entry.data['host']}",
        )

    @property
    def is_on(self) -> bool:
        """Return true if keylock is enabled."""
        settings_data = self.coordinator.data.get("settings", {})
        return settings_data.get("code", 0) == 1

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable keylock."""
        settings = {"code": 1}
        success = await self.coordinator.async_update_settings(settings)
        if success:
            await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable keylock."""
        settings = {"code": 0}
        success = await self.coordinator.async_update_settings(settings)
        if success:
            await self.coordinator.async_request_refresh()