"""Helper functions for FALS22 device info."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.const import CONF_NAME

from .const import DOMAIN, MANUFACTURER, MODEL


def get_device_info(config_entry) -> DeviceInfo:
    """Return device info for FALS22 device."""
    device_name = config_entry.data.get(CONF_NAME, config_entry.title)
    
    return DeviceInfo(
        identifiers={(DOMAIN, config_entry.entry_id)},
        name=device_name,
        manufacturer=MANUFACTURER,
        model=MODEL,
        sw_version="6.0+",
        configuration_url=f"http://{config_entry.data['host']}",
    )


def get_entity_name_prefix(config_entry) -> str:
    """Return the entity name prefix based on device name."""
    device_name = config_entry.data.get(CONF_NAME, config_entry.title)
    # Clean up the device name for entity IDs
    # Replace spaces, remove special characters, convert to lowercase
    prefix = device_name.lower()
    prefix = prefix.replace(" ", "_")
    prefix = prefix.replace("-", "_")
    # Remove any non-alphanumeric characters except underscores
    prefix = "".join(c for c in prefix if c.isalnum() or c == "_")
    return prefix
