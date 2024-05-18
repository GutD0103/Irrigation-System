import sys
import time
from Adafruit_IO import MQTTClient


class MyMQTTClient:
    def __init__(self, aio_username, aio_key, aio_feed_ids):
        self.aio_username = aio_username
        self.aio_key = aio_key
        self.aio_feed_ids = aio_feed_ids

        self.client = MQTTClient(self.aio_username, self.aio_key)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe

        self.processMessage = None

    def connected(self, client):
        print("Ket noi thanh cong ...")
        for feed in self.aio_feed_ids:
            self.client.subscribe(feed)

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribe thanh cong ...")

    def disconnected(self, client):
        print("Ngat ket noi ...")
        sys.exit(1)

    def message(self, client, feed_id, payload):
        print("Nhan du lieu: " + feed_id + ":" + payload)
        if self.processMessage != None:
            self.processMessage(feed_id,payload)

    def start(self):
        self.client.connect()
        self.client.loop_background()

    def publish_data(self, topic,data):
        self.client.publish(topic, data)

if __name__ == "__main__":
    AIO_USERNAME = "GutD"
    AIO_KEY = "aio_JskM93fdBC86QY0MvHnIugwvbHCh"
    AIO_FEED_ID = ["pump", "fan", "temperature", "humidity", "lux"]

    mqtt_client = MyMQTTClient(AIO_USERNAME, AIO_KEY, AIO_FEED_ID)
    mqtt_client.start()
    while True:
        mqtt_client.publish_data("temperature",100) 
        time.sleep(10)