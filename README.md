# FaLs22 - Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/DoctorExitus/ha-fals22.svg)](https://github.com/DoctorExitus/ha-fals22/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Home Assistant custom integration for FaLs22 Dewpoint Ventilation systems. This integration allows you to monitor and control your FaLs22 dewpoint ventilation system directly from Home Assistant.

## Features

- **Comprehensive Monitoring**: Track indoor/outdoor temperature, humidity (relative and absolute), operating hours, and system status
- **Remote Control**: Manual ventilation control, settings adjustment, and working hours configuration
- **Multi-language Support**: English and German localization
- **Local Control**: Works with FaLs22 webserver mode for local data access

## Supported FaLs22 Models

This integration is compatible with FaLs22 Dewpoint Ventilation systems running firmware version 6.0 and above.

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add `https://github.com/DoctorExitus/ha-fals22` as repository URL
5. Select "Integration" as category
6. Click "Add"
7. Search for "FaLs22" and install the integration
8. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/DoctorExitus/ha-fals22/releases)
2. Copy the `fals22` folder to your `custom_components` directory
3. Restart Home Assistant

## Configuration

### Device Setup

Before adding the integration to Home Assistant, ensure your FaLs22 device is properly configured:

1. **Standard Mode**: Device connects to your WiFi and sends data to the cloud (not supported)
2. **Webserver Mode**: Device runs a local webserver accessible via IP address (recommended)
3. **Access Point Mode**: Device creates its own WiFi network

Refer to your FaLs22 manual for detailed setup instructions.

### Home Assistant Integration Setup

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "FaLs22"
4. Enter a device name (used for entity naming, defaults to "FaLs22")
5. Enter your device's IP address
6. Optionally enter the device password if password protection is enabled
7. Complete the setup process

### Configuration Options

After adding the integration, you can configure additional options:

1. Click on the FaLs22 integration
2. Click on "Configure"
3. Adjust the following settings:
   - **Polling Interval**: How often to fetch data from the device (30-3600 seconds, default: 60)

## Entities

The integration creates the following entities (entity names will use your configured device name):

### Sensors
- **Indoor Temperature** (`sensor.[device_name]_indoor_temperature`)
- **Outdoor Temperature** (`sensor.[device_name]_outdoor_temperature`)
- **Indoor Relative Humidity** (`sensor.[device_name]_indoor_relative_humidity`)
- **Outdoor Relative Humidity** (`sensor.[device_name]_outdoor_relative_humidity`)
- **Indoor Absolute Humidity** (`sensor.[device_name]_indoor_absolute_humidity`)
- **Outdoor Absolute Humidity** (`sensor.[device_name]_outdoor_absolute_humidity`)
- **Operating Hours** (`sensor.[device_name]_operating_hours`)
- **Status Message** (`sensor.[device_name]_status_message`)

### Binary Sensors
- **Ventilation** (`binary_sensor.[device_name]_ventilation`) - Shows if ventilation is currently running

### Switches
- **Manual Mode** (`switch.[device_name]_manual_mode`) - Override the current Ventilation state for the duration set in the Manual Mode Duration entity
- **Keylock** (`switch.[device_name]_keylock`) - Enable/disable device keylock

### Number Controls
- **Manual Mode Duration** (`number.[device_name]_manual_mode_duration`) - Set custom duration for manual mode (0-300 minutes, defaults to 30 minutes)
- **Minimum Temperature** (`number.[device_name]_minimum_temperature`) - Set minimum operating temperature (0-35°C)
- **Maximum Temperature** (`number.[device_name]_maximum_temperature`) - Set maximum operating temperature (0-40°C)
- **Ventilation Duration** (`number.[device_name]_ventilation_duration`) - Set ventilation duration (0-99 min)
- **Break Duration** (`number.[device_name]_break_duration`) - Set break duration (0-90 min)
- **Target Humidity** (`number.[device_name]_target_humidity`) - Set target humidity (10-90%)
- **Humidity Difference** (`number.[device_name]_humidity_difference`) - Set humidity difference threshold (0.0-5.0 g/m³)

### Time Controls
- **Working Hours Start** (`time.[device_name]_working_hours_start`) - Set daily operation start time
- **Working Hours End** (`time.[device_name]_working_hours_end`) - Set daily operation end time

## Services

The integration provides the following services:

### Set Manual Ventilation
**Service**: `fals22.set_manual_ventilation`

Manually control ventilation with custom duration.

**Parameters**:
- `duration` (required): Duration in minutes (0-300)
- `turn_on` (required): Whether to turn ventilation on or off

**Example**:
```yaml
service: fals22.set_manual_ventilation
data:
  duration: 30
  turn_on: true
```

### Update Multiple Settings
**Service**: `fals22.update_multiple_settings`

Update multiple device settings simultaneously.

**Parameters**:
- `min_temp` (optional): Minimum temperature (0-35°C)
- `max_temp` (optional): Maximum temperature (0-40°C)
- `ventilation` (optional): Ventilation duration (0-99 min)
- `break` (optional): Break duration (0-90 min)
- `min_hum` (optional): Target humidity (10-90%)
- `difference` (optional): Humidity difference (0.0-5.0 g/m³)

**Example**:
```yaml
service: fals22.update_multiple_settings
data:
  min_temp: 15
  max_temp: 25
  min_hum: 50
```

## Automation Examples

### Basic Humidity Control
```yaml
automation:
  - alias: "High Humidity Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.fals22_indoor_relative_humidity
        above: 70
    action:
      - service: fals22.set_manual_ventilation
        data:
          duration: 60
          turn_on: true
```

### Temperature-Based Ventilation
```yaml
automation:
  - alias: "Temperature Ventilation Control"
    trigger:
      - platform: numeric_state
        entity_id: sensor.fals22_indoor_temperature
        above: 25
    condition:
      - condition: numeric_state
        entity_id: sensor.fals22_outdoor_temperature
        below: 20
    action:
      - service: fals22.set_manual_ventilation
        data:
          duration: 30
          turn_on: true
```

## Troubleshooting

### Connection Issues
- Verify the IP address is correct and the device is reachable
- Check if password protection is enabled and enter the correct password
- Ensure the device is in webserver mode if using local access
- Verify your Home Assistant instance can reach the device's network

### Authentication Errors
- Check if the device requires password authentication
- Verify the password is correct
- Ensure the device firmware supports the integration (version 6.0+)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to DNE Elektronik-Systeme Gmbh for creating the FaLs22 dewpoint ventilation system
- Home Assistant community for integration guidelines and support
- Claude Sonnet 4 which helped create this integration
