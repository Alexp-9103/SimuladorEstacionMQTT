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

# Function to generate dynamic station IDs
def generar_estaciones(cantidad):
    return [f"{i:03}" for i in range(1, cantidad + 1)]

# Get the number of stations dynamically
cantidad_estaciones = int(input("Ingrese la cantidad de estaciones a simular: "))
estaciones = generar_estaciones(cantidad_estaciones)
print(f"Generando {cantidad_estaciones} estaciones: {estaciones}")

# Connect to the broker
cliente = mqtt.Client()
cliente.connect(broker, port)
print(f"Conectado al broker {broker} en el puerto {port}")

try:
    while True:
        for estacion in estaciones:
            datos = generar_datos()
            for sensor, valor in datos.items():
                topic = f"/estacion/{estacion}/sensores/{sensor}"
                mensaje = f"{valor}"
                cliente.publish(topic, mensaje, qos=1)  # Use QoS level 1
                print(f"Publicado: {topic} -> {mensaje}")
                time.sleep(1)  # Pause between messages for each sensor
except KeyboardInterrupt:
    print("Simulación finalizada.")
