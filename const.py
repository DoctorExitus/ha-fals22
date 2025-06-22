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

# Sensor types with their properties and translation keys
SENSOR_TYPES = {
    # Temperature sensors
    "temp_in": {
        "translation_key": "temp_in",
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
        "data_key": "live",
    },
    "temp_out": {
        "translation_key": "temp_out",
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "icon": "mdi:thermometer",
        "data_key": "live",
    },
    # Humidity sensors
    "hum_in": {
        "translation_key": "hum_in",
        "native_unit_of_measurement": "%",
        "device_class": "humidity",
        "state_class": "measurement",
        "icon": "mdi:water-percent",
        "data_key": "live",
    },
    "hum_out": {
        "translation_key": "hum_out",
        "native_unit_of_measurement": "%", 
        "device_class": "humidity",
        "state_class": "measurement",
        "icon": "mdi:water-percent",
        "data_key": "live",
    },
    "abs_hum_in": {
        "translation_key": "abs_hum_in",
        "native_unit_of_measurement": "g/m³",
        "state_class": "measurement",
        "icon": "mdi:water",
        "data_key": "live",
    },
    "abs_hum_out": {
        "translation_key": "abs_hum_out",
        "native_unit_of_measurement": "g/m³",
        "state_class": "measurement", 
        "icon": "mdi:water",
        "data_key": "live",
    },
    # Status sensors
    "operating_hours": {
        "translation_key": "operating_hours",
        "native_unit_of_measurement": "h",
        "state_class": "total_increasing",
        "icon": "mdi:clock",
        "data_key": "live",
    },
    "message": {
        "translation_key": "message",
        "icon": "mdi:message-text",
        "data_key": "live",
    },
}

# Binary sensor for ventilation state
BINARY_SENSOR_TYPES = {
    "on": {
        "translation_key": "on",
        "device_class": "running",
        "icon": "mdi:fan",
        "data_key": "live",
    }
}

# Number entity types with translation keys
NUMBER_TYPES = {
    "min_temp": {
        "translation_key": "min_temp",
        "icon": "mdi:thermometer-low",
        "native_min_value": 0,
        "native_max_value": 35,
        "native_step": 1,
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
    },
    "max_temp": {
        "translation_key": "max_temp",
        "icon": "mdi:thermometer-high",
        "native_min_value": 0,
        "native_max_value": 40,
        "native_step": 1,
        "native_unit_of_measurement": "°C",
        "device_class": "temperature",
    },
    "ventilation": {
        "translation_key": "ventilation",
        "icon": "mdi:timer",
        "native_min_value": 0,
        "native_max_value": 99,
        "native_step": 1,
        "native_unit_of_measurement": "min",
        "device_class": "duration",
    },
    "break": {
        "translation_key": "break",
        "icon": "mdi:timer-pause",
        "native_min_value": 0,
        "native_max_value": 90,
        "native_step": 1,
        "native_unit_of_measurement": "min",
        "device_class": "duration",
    },
    "min_hum": {
        "translation_key": "min_hum",
        "icon": "mdi:water-percent",
        "native_min_value": 10,
        "native_max_value": 90,
        "native_step": 1,
        "native_unit_of_measurement": "%",
        "device_class": "humidity",
    },
    "difference": {
        "translation_key": "difference",
        "icon": "mdi:delta",
        "native_min_value": 0.0,
        "native_max_value": 5.0,
        "native_step": 0.1,
        "native_unit_of_measurement": "g/m³",
    },
}

# Time entity types with translation keys
TIME_TYPES = {
    "working_time_from": {
        "translation_key": "working_time_from",
        "icon": "mdi:clock-start",
        "hours_key": "working_hours_from",
        "minutes_key": "working_minutes_from",
    },
    "working_time_to": {
        "translation_key": "working_time_to",
        "icon": "mdi:clock-end", 
        "hours_key": "working_hours_to",
        "minutes_key": "working_minutes_to",
    },
}

# Switch entity types with translation keys
SWITCH_TYPES = {
    "manual_mode": {
        "translation_key": "manual_mode",
        "icon": "mdi:fan-auto",
    },
    "keylock": {
        "translation_key": "keylock",
        "icon": "mdi:lock",
    },
}