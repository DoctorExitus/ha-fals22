"""Support for FALS22 time entities."""
from __future__ import annotations

import logging
from datetime import time

from homeassistant.components.time import TimeEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, TIME_TYPES
from .device_helper import get_device_info, get_entity_name_prefix

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FALS22 time entities from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for time_type, time_config in TIME_TYPES.items():
        entities.append(FALS22TimeEntity(coordinator, config_entry, time_type, time_config))

    async_add_entities(entities)


class FALS22TimeEntity(CoordinatorEntity, TimeEntity):
    """Representation of a FALS22 time entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        config_entry: ConfigEntry,
        time_type: str,
        time_config: dict[str, str],
    ) -> None:
        """Initialize the time entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._time_type = time_type
        self._time_config = time_config
        
        # Generate entity ID based on device name
        entity_prefix = get_entity_name_prefix(config_entry)
        self._attr_unique_id = f"{config_entry.entry_id}_{time_type}"
        
        # Set translation key for localization
        if "translation_key" in time_config:
            self._attr_translation_key = time_config["translation_key"]
        
        self._attr_icon = time_config["icon"]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return get_device_info(self._config_entry)

    @property
    def native_value(self) -> time | None:
        """Return the current time value."""
        settings_data = self.coordinator.data.get("settings", {})
        
        hours = settings_data.get(self._time_config["hours_key"])
        minutes = settings_data.get(self._time_config["minutes_key"])
        
        if hours is not None and minutes is not None:
            return time(hour=hours, minute=minutes)
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_set_value(self, value: time) -> None:
        """Set new time value."""
        settings = {
            self._time_config["hours_key"]: value.hour,
            self._time_config["minutes_key"]: value.minute,
        }
        
        success = await self.coordinator.async_update_settings(settings)
        if success:
            # Update coordinator data immediately
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to update %s to %s", self._time_type, value)
