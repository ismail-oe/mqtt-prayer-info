import utime as time
from config import UTC_OFFSET

def hhmm_to_utc_seconds(hhmm):
    h, m = map(int, hhmm.split(":"))
    total = (h - UTC_OFFSET) * 3600 + m * 60
    return total % (24 * 3600)

def current_utc_seconds():
    t = time.gmtime()
    return t[3] * 3600 + t[4] * 60 + t[5]