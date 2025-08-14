from umqtt.simple import MQTTClient
import utime as time

class MqttService:
    def __init__(self, client_name, broker_addr, keepalive, topics, callback):
        self.client_name = client_name
        self.broker_addr = broker_addr
        self.keepalive   = keepalive
        self.topics      = topics
        self.callback    = callback
        self.client      = None
        self.last_io     = 0

    def connect_and_sub(self):
        if self.client:
            try:
                self.client.disconnect()
            except:
                pass
        c = MQTTClient(self.client_name, self.broker_addr, keepalive=self.keepalive)
        c.set_callback(self.callback)
        c.connect()
        for t in self.topics:
            c.subscribe(t)
        self.client  = c
        self.last_io = time.time()
        print("MQTT connected, subscribed:", self.topics)

    def disconnect(self):
        if self.client:
            try:
                self.client.disconnect()
            except:
                pass

    def loop_once(self, ping_every=30):
        self.client.check_msg()
        now = time.time()
        if now - self.last_io >= ping_every:
            try:
                self.client.ping()
            except AttributeError:
                pass
            self.last_io = now

    def touch_io(self):
        self.last_io = time.time()