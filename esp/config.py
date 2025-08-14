# Configuration

# Wi-Fi
WIFI_SSID = "SSID"
WIFI_PSK  = "PASSWORD"

# MQTT
BROKER_ADDR    = "IP-ADDRESS"
CLIENT_NAME    = "ID"
KEEPALIVE      = 60
PING_EVERY     = 30

# Topics
TOPIC_TODAY    = b"mqtt-prayer-info/times/today"
TOPIC_TOMORROW = b"mqtt-prayer-info/times/tomorrow"
TOPICS = [TOPIC_TODAY, TOPIC_TOMORROW]

# Hardware
LED_PIN = 2

# Time settings
UTC_OFFSET = 2