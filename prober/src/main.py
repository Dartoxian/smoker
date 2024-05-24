import json
from machine import Pin, PWM, reset

import wifi
from max6675 import MAX6675
from umqtt.simple import MQTTClient
import time

import ssl
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.verify_mode = ssl.CERT_NONE

led = Pin("LED", Pin.OUT)

# A second is needed to let the buzzer start up it seems
time.sleep(1)
buzzer = None
button = Pin(1, Pin.OUT)


def button_handler(pin: Pin):
    global buzzer
    if buzzer:
        buzzer.deinit()
        buzzer = None
    else:
        buzzer = PWM(Pin(0), duty_u16=32767)


button.irq(trigger=Pin.IRQ_RISING, handler=button_handler)
sensor1 = MAX6675(Pin(2, Pin.OUT), Pin(3, Pin.OUT), Pin(4, Pin.IN))
sensor2 = MAX6675(Pin(10, Pin.OUT), Pin(11, Pin.OUT), Pin(12, Pin.IN))

try:
    wifi.connect()
except KeyboardInterrupt:
    reset()

mqtt_host = "2fc390f34bf5428cb7f53c0350f2466c.s1.eu.hivemq.cloud"
mqtt_username = "smoker"
mqtt_password = "asdf23asaGHJ"
mqtt_publish_topic = "smoker"

# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "smoker-01"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
    client_id=mqtt_client_id,
    server=mqtt_host,
    port=8883,
    ssl=ssl_context,
    user=mqtt_username,
    password=mqtt_password)

mqtt_client.connect()


while True:
    led.toggle()
    sensor1_temp = sensor1.read()
    sensor2_temp = sensor2.read()
    print(f"temperature1={sensor1_temp}")
    print(f"temperature2={sensor2_temp}")
    mqtt_client.publish(mqtt_publish_topic, json.dumps({"temp1": sensor1_temp, "temp2": sensor2_temp}))

    if buzzer:
        buzzer.freq(int(sensor1_temp) * 20)

    time.sleep(1)
