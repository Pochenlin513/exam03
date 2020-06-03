import paho.mqtt.client as paho
import serial
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
x = []
y = []
z = []
tilt = []
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

serdev2 = '/dev/ttyACM0'
s2 = serial.Serial(serdev2, 9600)

    

"""
def accHandle():
    while len(data) < 20:
        linex=s2.readline() # Read an echo string from K66F terminated with '\n'
        #print(linex)
        mqttc.publish(topic, linex)
        x.append(float(linex))
        liney=s2.readline() # Read an echo string from K66F terminated with '\n'
        #print(liney)
        mqttc.publish(topic2, liney)
        y.append(float(liney))
        linez=s2.readline() # Read an echo string from K66F terminated with '\n'
        #print(linez)
        mqttc.publish(topic3, linez)
        z.append(float(linez))
        linet=s2.readline() # Read an echo string from K66F terminated with '\n'
        #print(linet)
        mqttc.publish(topic4, linet)
        tilt.append(float(linet))
    
    #print(len(tilt))
"""

mqttc = paho.Client()


# Settings for connection
# TODO: revise host to your ip
host = "localhost"
topic = "velocity"


data = []
# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")


def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
      print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)




# XBee setting

s.write("+++".encode())
char = s.read(3)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x140\r\n".encode())
char = s.read(3)
print("Set MY <BASE_MY>.")
print(char.decode())

s.write("ATDL 0x240\r\n".encode())
char = s.read(3)
print("Set DL <BASE_DL>.")
print(char.decode())

s.write("ATID 0x27\r\n".encode())
char = s.read(3)
print("Set PAN ID <PAN_ID>.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")


# Publish messages from Python
"""
num = 0
while num != 5:
      ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
      if (ret[0] != 0):
            print("Publish failed")
      mqttc.loop()
      time.sleep(1.5)
      num += 1

# Loop forever, receiving messages
"""

s.write("\r".encode())
time.sleep(1)
s.write("/sendBatch/run\r".encode())
time.sleep(1)
size = int(s2.readline())
i = 0
veldata = []
while i < size:
    line = s2.readline()
    mqttc.publish(topic, line)

"""
while i>0:
    print("hi")
    #mqttc.loop()
    #mqttc2.loop()
    #print(data)
    s.write("/getStatus/run\r".encode())
    line = s.readline()
    print(line)
    time.sleep(1)
"""