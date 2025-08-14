import network
import utime as time

def wait_wifi(ssid, psk, timeout_s=20):
    sta = network.WLAN(network.STA_IF)
    if not sta.active():
        sta.active(True)
    if not sta.isconnected():
        sta.connect(ssid, psk)
        t0 = time.ticks_ms()
        while not sta.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > timeout_s * 1000:
                raise OSError("Wi-Fi connection timeout")
            time.sleep_ms(100)
    print("Wi-Fi:", sta.ifconfig())
    return sta