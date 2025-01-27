import random
import time
import paho.mqtt.client as mqtt


broker = "mqtt.eclipseprojects.io"  #
port = 1883


def generar_datos():
    return {
        "temperatura": round(random.uniform(-10, 40), 2), 
        "humedad": random.randint(10, 100),  
        "viento": round(random.uniform(0, 20), 2),
        "presion": random.randint(950, 1050)  
    }


cliente = mqtt.Client()
cliente.connect(broker, port)
print(f"Conectado al broker {broker} en el puerto {port}")


estaciones = ["001", "002", "003"]  

try:
    while True:
        for estacion in estaciones:
            datos = generar_datos()
            for sensor, valor in datos.items():
                topic = f"/estacion/{estacion}/sensores/{sensor}"
                mensaje = f"{valor}"
                cliente.publish(topic, mensaje, qos=1)  
                print(f"Publicado: {topic} -> {mensaje}")
                time.sleep(2) 
except KeyboardInterrupt:
    print("Simulación finalizada.")
