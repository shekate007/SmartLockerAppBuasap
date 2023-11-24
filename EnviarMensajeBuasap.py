import machine
import time
import urequests

# Configuración de la red WiFi
SSID = "Jorge"
PASSWORD = "12345"

# Token de acceso para la API de WhatsApp
TOKEN = "Bearer EAAIao2QuMP4BAEg4Hs76IvHZAeBuZCYP9lCnipU1hlxDmTcw77orMZCaawAoAusMNvvDlETU5d1uxiwjvB72j2DW6UOJqxIxZCofP6apbuitVtZBjueB4HZBXZBhIY64JN75tWFVY1UQbBo9gZAZBWl776gC3khAPcgO4tiykQ1CPpZBXTBCEeRZB49dSUgZB2rYW2OYr7NWKgzEIgZDZD"

# URL a donde se enviarán los mensajes de WhatsApp
SERVIDOR = "https://graph.facebook.com/v17.0/184761381381361/messages"

# Número de teléfono al que se enviará el mensaje
NUMERO_TELEFONO = "523333979218"

# JSON con el mensaje a enviar
payload = {
    "messaging_product": "whatsapp",
    "to": NUMERO_TELEFONO,
    "type": "text",
    "text": {"body": "Se ha abierto el Locker desde la App"}
}

# Pin del sensor de movimiento
pinSensorMov = machine.Pin(15, machine.Pin.IN)

def conectar_wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Conectado a la red WiFi")
    print("IP:", wlan.ifconfig()[0])

def enviar_mensaje_whatsapp():
    if pinSensorMov.value() == 1:  # Si hay movimiento
        print("Hay movimiento")
        time.sleep(5)  # Esperar 5 segundos

        # Configurar la conexión HTTP
        headers = {
            "Content-Type": "application/json",
            "Authorization": TOKEN
        }

        # Enviar el mensaje
        response = urequests.post(SERVIDOR, json=payload, headers=headers)

        if response.status_code == 200:
            print("Mensaje enviado con éxito")
            print("Respuesta del servidor:", response.text)
        else:
            print("Error al enviar el mensaje")
            print("Código de respuesta:", response.status_code)

        response.close()

conectar_wifi()

while True:
    enviar_mensaje_whatsapp()
    time.sleep(1)  # Esperar 1 segundo