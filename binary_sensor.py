"""Support for FALS22 binary sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass
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
    """Set up FALS22 binary sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    binary_sensors = [
        FALS22VentilationBinarySensor(coordinator, config_entry),
    ]

    async_add_entities(binary_sensors)


class FALS22VentilationBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Binary sensor for FALS22 ventilation state."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, config_entry: ConfigEntry) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_ventilation_running"
        self._attr_translation_key = "on"
        self._attr_device_class = BinarySensorDeviceClass.RUNNING
        self._attr_icon = "mdi:fan"

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
    def is_on(self) -> bool | None:
        """Return true if the ventilation is running."""
        live_data = self.coordinator.data.get("live", {})
        
        if not live_data:
            return None
        
        is_on = live_data.get("on")
        if is_on is None:
            return None
            
        return is_on == 1

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success 
            and self.coordinator.data.get("live") is not None
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        live_data = self.coordinator.data.get("live", {})
        settings_data = self.coordinator.data.get("settings", {})
        
        if not live_data:
            return None

        return {
            "operating_hours": live_data.get("operating_hours", 0),
            "message": live_data.get("message", "").strip(),
            "ventilation_duration": settings_data.get("ventilation", 0),
            "break_duration": settings_data.get("break", 0),
            "keylock_enabled": settings_data.get("code", 0) == 1,
        }