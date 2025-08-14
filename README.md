# mqtt-prayer-info

MQTT-based system for distributing Islamic prayer times.  
Includes a Raspberry Pi publisher and ESP32/ESP8266 MicroPython client.

## Features
- Publishes daily prayer times as JSON via MQTT
- ESP client parses data and shows countdown to next prayer
- Automatic Wi-Fi and MQTT reconnect
- Modular: config, Wi-Fi, MQTT, and time utilities in separate files
- Raspberry Pi script can be run automatically via **cron** every day at midnight

## Structure
```
mqtt-prayer-info/
├── esp/              # MicroPython ESP client
│   ├── config.py
│   ├── wifi_service.py
│   ├── mqtt_service.py
│   ├── time_utils.py
│   ├── time_sync.py
│   └── main.py
├── pi/               # Raspberry Pi publisher
│   ├── config.json
│   ├── main.py
│   └── ressources/
│       └── times_sampleCity.json
```

## Setup

### Raspberry Pi
1. Install requirements:
   ```bash
   pip install paho-mqtt
   ```
2. Configure `pi/config.json`.
3. (Optional) Set up cronjob to run daily at 00:00:
   ```bash
   crontab -e
   ```
   Add the following line:
   ```
   0 0 * * * /usr/bin/python3 /path/to/mqtt-prayer-info/pi/main.py
   ```
4. Run manually if needed:
   ```bash
   cd pi
   python3 main.py
   ```

### ESP32/ESP8266
1. Flash MicroPython firmware ([download](https://micropython.org/download/)).
2. Edit `esp/config.py` with Wi-Fi & MQTT settings.
3. Upload:
   ```bash
   cd esp
   mpremote connect /dev/ttyUSB0 cp -r ./ :
   ```
4. Reset board — `main.py` runs automatically.

## MQTT Topics
- `mqtt-prayer-info/times/today`
- `mqtt-prayer-info/times/tomorrow`

Example payload:
```json
{
  "imsak": "03:15",
  "fajr": "03:35",
  "sunrise": "06:05",
  "dhuhr": "13:42",
  "asr": "17:44",
  "maghrib": "21:09",
  "isha": "23:27",
  "date": "2025-08-10"
}
```

## Example Output
```
Wi-Fi connected: 192.168.178.45
MQTT connected
Next: fajr at 03:35 in 4h 12m 15s
```