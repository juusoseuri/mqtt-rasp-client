import time
import json
import paho.mqtt.client as paho
from paho import mqtt
from envirophat import *

# set your broker here
# broker = ???
port = 8883
topic = 'button/'

def on_connect(client, userdata, flags, rc, properties=None):
    if (rc == 0):
        client.connected_flag = True
        print("Connected OK Returned code =",rc)
    else:
        print("Connection failed with code =",rc)

def __main__():
        
    # Initialise client
    client = paho.Client(client_id="distance", userdata=None, protocol=paho.MQTTv311)
    client.on_connect = on_connect

    print("Connecting to broker: ", broker)
    
    # enable TLS
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

    # Set username and password
    client.username_pw_set("username", "password")
    
    # Set flag
    client.connected_flag = False

    # Connect to the broker
    client.connect(broker, port)

    # React to publishing
    
    # Start hte loop
    client.loop_start()
    
    # Wait until connected
    while not client.connected_flag:
        print("In wait loop")
        time.sleep(1)

    print("MQTT connected! \nIn Main loop")
    
    distance = 0

    try:
        while True:
            acceleration = motion.accelerometer()
            telemetry = json.dumps({"light":light.raw(),"temperature":weather.temperature(),"acceleration":[acceleration.x,acceleration.y,acceleration.z]})
            print("Sending data", telemetry)
            client.publish(topic, telemetry)
            print("Data sent")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting program")
        client.loop_stop()
        client.disconnect()
        
__main__()
