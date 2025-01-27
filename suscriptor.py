import time
import paho.mqtt.client as mqtt

broker = "mqtt.eclipseprojects.io"
port = 1883

def on_message(client, userdata, message):
    try:
        topic = message.topic
        payload = message.payload.decode("utf-8")
        print(f"Recibido: {topic} -> {payload}")

        # Optionally log to a file
        with open("subscriber.log", "a") as log_file:
            log_file.write(f"{time.ctime()} - Received: {topic} -> {payload}\n")
    except Exception as e:
        print(f"Error processing message: {e}")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado exitosamente al broker.")

        client.subscribe("/estacion/+/sensores/#", qos=1)
        print("Suscrito al topic /estacion/+/sensores/#")
    else:
        print(f"Conexión fallida con código de error {rc}")

def on_disconnect(client, userdata, rc):
    print(f"Desconectado del broker, código de desconexión: {rc}")

    if rc != 0:
        print("Intentando reconectar...")
        try:
            client.reconnect()
        except Exception as e:
            print(f"Error de reconexión: {e}")


cliente = mqtt.Client()
cliente.on_message = on_message
cliente.on_connect = on_connect  
cliente.on_disconnect = on_disconnect  
cliente.connect(broker, port)
print(f"Conectado al broker {broker} en el puerto {port}")


cliente.subscribe("/estacion/+/sensores/#", qos=1)  
print("Suscrito al topic /estacion/+/sensores/#")


cliente.loop_start()  


try:
    while True:
        time.sleep(1)  
except KeyboardInterrupt:
    print("Suscripción terminada.")
    cliente.loop_stop() 
