"""Support for FALS22 sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SENSOR_TYPES
from .device_helper import get_device_info, get_entity_name_prefix

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up FALS22 sensors from a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    sensors = []
    for sensor_type, sensor_config in SENSOR_TYPES.items():
        sensors.append(FALS22Sensor(coordinator, config_entry, sensor_type, sensor_config))

    async_add_entities(sensors)


class FALS22Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a FALS22 sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator,
        config_entry: ConfigEntry,
        sensor_type: str,
        sensor_config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        
        # Generate entity ID based on device name
        entity_prefix = get_entity_name_prefix(config_entry)
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        
        # Set translation key for localization
        if "translation_key" in sensor_config:
            self._attr_translation_key = sensor_config["translation_key"]
        
        # Set sensor properties
        if "native_unit_of_measurement" in sensor_config:
            self._attr_native_unit_of_measurement = sensor_config["native_unit_of_measurement"]
        if "device_class" in sensor_config:
            self._attr_device_class = sensor_config["device_class"]
        if "state_class" in sensor_config:
            self._attr_state_class = sensor_config["state_class"]
        if "icon" in sensor_config:
            self._attr_icon = sensor_config["icon"]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return get_device_info(self._config_entry)

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        data_key = self._sensor_config["data_key"]
        data = self.coordinator.data.get(data_key, {})
        
        if not data:
            return None
            
        value = data.get(self._sensor_type)
        
        # Handle special cases
        if self._sensor_type == "message" and isinstance(value, str):
            # Clean up message text
            return value.strip()
        
        return value

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        if self._sensor_type == "temp_in":
            # Add datetime info for the main temperature sensor
            live_data = self.coordinator.data.get("live", {})
            if live_data:
                return {
                    "last_update": f"{live_data.get('day', 0):02d}.{live_data.get('month', 0):02d}.{live_data.get('year', 0)} {live_data.get('hours', 0):02d}:{live_data.get('minutes', 0):02d}",
                    "working_hours_from": f"{self.coordinator.data.get('settings', {}).get('working_hours_from', 0):02d}:{self.coordinator.data.get('settings', {}).get('working_minutes_from', 0):02d}",
                    "working_hours_to": f"{self.coordinator.data.get('settings', {}).get('working_hours_to', 0):02d}:{self.coordinator.data.get('settings', {}).get('working_minutes_to', 0):02d}",
                }
        return None


# End of sensor.py
