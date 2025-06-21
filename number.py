"""Number entities for dewpoint ventilation system settings."""
import logging
from typing import Any

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DewpointCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up dewpoint number entities."""
    coordinator: DewpointCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = [
        DewpointHumidityTarget(coordinator),
        DewpointVentilationDuration(coordinator),
        DewpointVentilationBreak(coordinator),
    ]
    
    async_add_entities(entities)


class DewpointNumberEntity(CoordinatorEntity, NumberEntity):
    """Base class for dewpoint number entities."""
    
    def __init__(self, coordinator: DewpointCoordinator, key: str, name: str) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._key = key
        self._attr_name = f"Dewpoint {name}"
        self._attr_unique_id = f"{coordinator.host}_{key}"
        self._attr_device_info = coordinator.device_info

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success and self.coordinator.data is not None

    async def async_set_native_value(self, value: float) -> None:
        """Set the number value."""
        try:
            await self.coordinator.set_setting(self._key, value)
            # Trigger coordinator update to reflect changes
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Failed to set %s to %s: %s", self._key, value, err)
            raise


class DewpointHumidityTarget(DewpointNumberEntity):
    """Humidity target number entity."""
    
    def __init__(self, coordinator: DewpointCoordinator) -> None:
        """Initialize humidity target."""
        super().__init__(coordinator, "min_hum", "Humidity Target")
        self._attr_icon = "mdi:water-percent"
        self._attr_native_min_value = 10
        self._attr_native_max_value = 90
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = "%"
        self._attr_mode = NumberMode.SLIDER

    @property
    def native_value(self) -> float | None:
        """Return current humidity target."""
        if self.coordinator.data and "settings" in self.coordinator.data:
            return self.coordinator.data["settings"].get("min_hum")
        return None


class DewpointVentilationDuration(DewpointNumberEntity):
    """Ventilation duration number entity."""
    
    def __init__(self, coordinator: DewpointCoordinator) -> None:
        """Initialize ventilation duration."""
        super().__init__(coordinator, "ventilation", "Ventilation Duration")
        self._attr_icon = "mdi:timer"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 99
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = "min"
        self._attr_mode = NumberMode.BOX

    @property
    def native_value(self) -> float | None:
        """Return current ventilation duration."""
        if self.coordinator.data and "settings" in self.coordinator.data:
            return self.coordinator.data["settings"].get("ventilation")
        return None


class DewpointVentilationBreak(DewpointNumberEntity):
    """Ventilation break number entity."""
    
    def __init__(self, coordinator: DewpointCoordinator) -> None:
        """Initialize ventilation break."""
        super().__init__(coordinator, "break", "Ventilation Break")
        self._attr_icon = "mdi:timer-pause"
        self._attr_native_min_value = 0
        self._attr_native_max_value = 90
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = "min"
        self._attr_mode = NumberMode.BOX

    @property
    def native_value(self) -> float | None:
        """Return current ventilation break."""
        if self.coordinator.data and "settings" in self.coordinator.data:
            return self.coordinator.data["settings"].get("break")
        return None
