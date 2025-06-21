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

from .const import DOMAIN, MANUFACTURER, MODEL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FALS22 switches from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    switches = [
        FALS22ManualVentilationSwitch(coordinator, config_entry),
    ]

    async_add_entities(switches)


class FALS22ManualVentilationSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of FALS22 manual ventilation switch."""

    def __init__(self, coordinator, config_entry: ConfigEntry) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_name = "FALS22 Manual Ventilation"
        self._attr_unique_id = f"{config_entry.entry_id}_manual_ventilation"
        self._attr_icon = "mdi:fan-auto"

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
        """Return true if the switch is on."""
        live_data = self.coordinator.data.get("live", {})
        if not live_data:
            return False
        
        # Check if ventilation is currently running
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
        else:
            _LOGGER.error("Failed to turn on manual ventilation")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off manual ventilation for 30 minutes."""
        success = await self.coordinator.async_set_manual_mode(30, False)
        if success:
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to turn off manual ventilation")

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        live_data = self.coordinator.data.get("live", {})
        if not live_data:
            return None

        return {
            "status_message": live_data.get("message", "").strip(),
            "operating_hours": live_data.get("operating_hours", 0),
        }