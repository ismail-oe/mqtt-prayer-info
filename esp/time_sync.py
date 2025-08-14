import utime as time

def sync_utc(ntp_host="pool.ntp.org", tries=3, delay_s=1):
    import ntptime
    ntptime.host = ntp_host
    for _ in range(tries):
        try:
            ntptime.settime()  # sets RTC to UTC
            t = time.gmtime()
            print("NTP OK (UTC): {:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5]))
            return True
        except OSError as e:
            print("NTP retry:", e)
            time.sleep(delay_s)
    print("NTP failed")
    return False