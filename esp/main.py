from time_sync import sync_utc
from machine import Pin
import ujson as json
import utime as time

from config import (
    WIFI_SSID, WIFI_PSK,
    BROKER_ADDR, CLIENT_NAME,
    KEEPALIVE, PING_EVERY,
    TOPICS, TOPIC_TODAY, TOPIC_TOMORROW,
    LED_PIN
)
from wifi_service import wait_wifi
from mqtt_service import MqttService
from time_utils import hhmm_to_utc_seconds, current_utc_seconds

led = Pin(LED_PIN, Pin.OUT)
led.value(1)

times_today = None
times_tomorrow = None

def blink(times=2, interval_ms=120):
    for _ in range(times):
        led.value(0); time.sleep_ms(interval_ms)
        led.value(1); time.sleep_ms(interval_ms)

def on_message(topic, msg):
    mqtt.touch_io()
    global times_today, times_tomorrow
    try:
        data = json.loads(msg)
    except Exception as e:
        print("JSON parse error:", e)
        return
    if topic == TOPIC_TODAY:
        times_today = data
    elif topic == TOPIC_TOMORROW:
        times_tomorrow = data
    blink(2, 80)

def do_data():
    if not times_today:
        return

    now_sec = current_utc_seconds()
    next_delta = 24 * 3600
    next_event = None

    for name, val in times_today.items():
        if not isinstance(val, str) or ":" not in val:  # skip e.g. "date"
            continue
        event_sec = hhmm_to_utc_seconds(val)
        delta = (event_sec - now_sec) % (24 * 3600)
        if delta < next_delta:
            next_delta = delta
            next_event = (name, val)

    if next_event:
        h = next_delta // 3600
        m = (next_delta % 3600) // 60
        s = next_delta % 60
        print("Next:", next_event[0], "at", next_event[1], "in", "{}h {}m {}s".format(h, m, s))

wait_wifi(WIFI_SSID, WIFI_PSK)
sync_utc()

mqtt = MqttService(
    client_name = CLIENT_NAME,
    broker_addr = BROKER_ADDR,
    keepalive   = KEEPALIVE,
    topics      = TOPICS,
    callback    = on_message
)
mqtt.connect_and_sub()

while True:
    try:
        mqtt.loop_once(ping_every=PING_EVERY)
        do_data()
        time.sleep(1)
    except OSError as e:
        print("MQTT error:", e, "-> reconnecting...")
        time.sleep_ms(500)
        try:
            mqtt.connect_and_sub()
        except Exception as e2:
            print("Reconnect failed:", e2)
            time.sleep_ms(1500)
