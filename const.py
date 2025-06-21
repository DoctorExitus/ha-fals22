"""Constants for the FALS22 integration."""

DOMAIN = "fals22"

# Configuration keys
CONF_HOST = "host"
CONF_PASSWORD = "password"

# Default values
DEFAULT_NAME = "FALS22 Dewpoint Ventilation"
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes

# Device info
MANUFACTURER = "FALS22"
MODEL = "Dewpoint Ventilation System"

# Sensor types with their properties
SENSOR_TYPES = {
    # Temperature sensors
    "temp_in": {
        "name": "Indoor Temperature",
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
        "data_key": "live",
    },
    "temp_out": {
        "name": "Outdoor Temperature", 
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
        "data_key": "live",
    },
    # Humidity sensors
    "hum_in": {
        "name": "Indoor Relative Humidity",
        "native_unit_of_measurement": "%",
        "device_class": "humidity",
        "state_class": "measurement",
        "icon": "mdi:water-percent",
        "data_key": "live",
    },
    "hum_out": {
        "name": "Outdoor Relative Humidity",
        "native_unit_of_measurement": "%", 
        "device_class": "humidity",
        "state_class": "measurement",
        "icon": "mdi:water-percent",
        "data_key": "live",
    },
    "abs_hum_in": {
        "name": "Indoor Absolute Humidity",
        "native_unit_of_measurement": "g/m³",
        "state_class": "measurement",
        "icon": "mdi:water",
        "data_key": "live",
    },
    "abs_hum_out": {
        "name": "Outdoor Absolute Humidity",
        "native_unit_of_measurement": "g/m³",
        "state_class": "measurement", 
        "icon": "mdi:water",
        "data_key": "live",
    },
    # Status sensors
    "operating_hours": {
        "name": "Operating Hours",
        "native_unit_of_measurement": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock",
        "data_key": "live",
    },
    "message": {
        "name": "Status Message",
        "icon": "mdi:message-text",
        "data_key": "live",
    },
    # Settings sensors
    "min_temp": {
        "name": "Minimum Temperature Setting",
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
        "icon": "mdi:thermometer-low",
        "data_key": "settings",
    },
    "max_temp": {
        "name": "Maximum Temperature Setting", 
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
        "icon": "mdi:thermometer-high",
        "data_key": "settings",
    },
    "ventilation": {
        "name": "Ventilation Duration Setting",
        "native_unit_of_measurement": "min",
        "icon": "mdi:timer",
        "data_key": "settings",
    },
    "break": {
        "name": "Break Duration Setting",
        "native_unit_of_measurement": "min", 
        "icon": "mdi:timer-off",
        "data_key": "settings",
    },
    "min_hum": {
        "name": "Target Humidity Setting",
        "native_unit_of_measurement": "%",
        "device_class": "humidity",
        "icon": "mdi:target",
        "data_key": "settings",
    },
    "difference": {
        "name": "Absolute Humidity Difference Setting",
        "native_unit_of_measurement": "g/m³",
        "icon": "mdi:delta",
        "data_key": "settings",
    },
}

# Binary sensor for ventilation state
BINARY_SENSOR_TYPES = {
    "on": {
        "name": "Ventilation Active",
        "device_class": "running",
        "icon": "mdi:fan",
        "data_key": "live",
    }
}