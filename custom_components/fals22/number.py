"""Support for FALS22 number entities."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NUMBER_TYPES
from .device_helper import get_device_info, get_entity_name_prefix

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FALS22 number entities from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for number_type, number_config in NUMBER_TYPES.items():
        entities.append(FALS22NumberEntity(coordinator, config_entry, number_type, number_config))
    
    # Add manual duration entity
    entities.append(FALS22ManualDurationEntity(coordinator, config_entry))

    async_add_entities(entities)


class FALS22NumberEntity(CoordinatorEntity, NumberEntity):
    """Representation of a FALS22 number entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        config_entry: ConfigEntry,
        number_type: str,
        number_config: dict[str, Any],
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._number_type = number_type
        
        # Generate entity ID based on device name
        entity_prefix = get_entity_name_prefix(config_entry)
        self._attr_unique_id = f"{config_entry.entry_id}_{number_type}"
        
        # Set translation key for localization
        if "translation_key" in number_config:
            self._attr_translation_key = number_config["translation_key"]
        
        # Set number properties
        self._attr_icon = number_config["icon"]
        self._attr_native_min_value = number_config["native_min_value"]
        self._attr_native_max_value = number_config["native_max_value"]
        self._attr_native_step = number_config["native_step"]
        self._attr_native_unit_of_measurement = number_config.get("native_unit_of_measurement")
        
        if "device_class" in number_config:
            self._attr_device_class = number_config["device_class"]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return get_device_info(self._config_entry)

    @property
    def native_value(self) -> float | None:
        """Return the current value."""
        settings_data = self.coordinator.data.get("settings", {})
        return settings_data.get(self._number_type)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        settings = {self._number_type: value}
        
        success = await self.coordinator.async_update_settings(settings)
        if success:
            # Update coordinator data immediately
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to update %s to %s", self._number_type, value)


class FALS22ManualDurationEntity(CoordinatorEntity, NumberEntity):
    """Representation of manual mode duration entity."""

    _attr_has_entity_name = True
    _attr_translation_key = "manual_duration"
    _attr_icon = "mdi:timer-play"
    _attr_native_min_value = 5
    _attr_native_max_value = 300
    _attr_native_step = 5
    _attr_native_unit_of_measurement = "min"
    _attr_device_class = "duration"

    def __init__(self, coordinator, config_entry: ConfigEntry) -> None:
        """Initialize the manual duration entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        
        # Generate entity ID based on device name
        entity_prefix = get_entity_name_prefix(config_entry)
        self._attr_unique_id = f"{config_entry.entry_id}_manual_duration"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return get_device_info(self._config_entry)

    @property
    def native_value(self) -> float:
        """Return the current value."""
        return self.coordinator.data.get("manual_duration", 30)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    async def async_set_native_value(self, value: float) -> None:
        """Set new value."""
        # Store the manual duration in coordinator data
        self.coordinator.data["manual_duration"] = int(value)
        # Notify listeners that data has changed
        self.coordinator.async_set_updated_data(self.coordinator.data)
