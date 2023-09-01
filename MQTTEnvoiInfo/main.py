import RPi.GPIO as GPIO
import dht11
import paho.mqtt.client as mqtt
import time

# Configuration des broches GPIO
DHT_PIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Initialisation du capteur DHT11
instance = dht11.DHT11(pin=DHT_PIN)

# Configuration du client MQTT
MQTT_BROKER = "10.4.1.42"
MQTT_TOPIC = "jacob/temperature/sensor"  # Sujet spécifique pour la température
client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion MQTT établie avec succès.")
    else:
        print("Échec de la connexion MQTT, code de retour : " + str(rc))


client.on_connect = on_connect
client.connect(MQTT_BROKER, 1883, 60)

try:
    while True:
        # Lecture des données du capteur DHT11
        result = instance.read()

        if result.is_valid():
            temperature = result.temperature

            # Publication de la température sur MQTT avec une QoS de 0
            client.publish(MQTT_TOPIC, str(temperature), qos=0)
            print("Température publiée sur MQTT : " + str(temperature))
        else:
            print("test")
        # Pause entre les lectures
        client.loop()
        time.sleep(5)  # Vous pouvez ajuster la fréquence des lectures ici

except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    print("Arrêt du programme.")
