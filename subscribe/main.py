import time
import paho.mqtt.client as mqtt

# Callback function for connecting to the MQTT server
def on_connect(client, userdata, flags, rc):
    print(flags)
    if rc == 0:
        print("Connected to the MQTT server")
        client.subscribe(MQTT_TOPIC, qos=1)  # Subscribe to the topic "jacob/temperature/sensor"
        print("Subscribed to " + MQTT_TOPIC)
    else:
        print(f"Failed to connect to the MQTT server with error code: {rc}")

# Callback function for receiving MQTT messages
def on_message(client, userdata, msg):
    print(f"Message received on topic '{msg.topic}': {msg.payload.decode()}")

# Create an MQTT client
MQTT_BROKER = "10.4.1.42"
MQTT_TOPIC = "jacob/temperature/sensor"
client = mqtt.Client(client_id="unique_client_id", clean_session=False)  # Set a unique client ID and clean_session to False

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT server at the specified address
client.connect(MQTT_BROKER, 1883, 60)

# Main loop to maintain the connection and process messages
try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    print("Disconnected from the MQTT server")
