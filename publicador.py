import random
import time
import paho.mqtt.client as mqtt

# MQTT broker configuration
broker = "mqtt.eclipseprojects.io"  # You can use "test.mosquitto.org" as well
port = 1883

# Function to generate random sensor data
def generar_datos():
    return {
        "temperatura": round(random.uniform(-10, 40), 2),  # Temperature in °C
        "humedad": random.randint(10, 100),  # Humidity in %
        "viento": round(random.uniform(0, 20), 2),  # Wind speed in m/s
        "presion": random.randint(950, 1050)  # Atmospheric pressure in hPa
    }

# Connect to the broker
cliente = mqtt.Client()
cliente.connect(broker, port)
print(f"Conectado al broker {broker} en el puerto {port}")

# Simulate multiple weather stations
estaciones = ["001", "002", "003"]  # Can be configurable

try:
    while True:
        for estacion in estaciones:
            datos = generar_datos()
            for sensor, valor in datos.items():
                topic = f"/estacion/{estacion}/sensores/{sensor}"
                mensaje = f"{valor}"
                cliente.publish(topic, mensaje, qos=1)  # Use QoS level 1
                print(f"Publicado: {topic} -> {mensaje}")
                time.sleep(2)  # Increased sleep to allow subscriber to catch up
except KeyboardInterrupt:
    print("Simulación finalizada.")
