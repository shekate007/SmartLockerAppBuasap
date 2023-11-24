import machine
import time
import urequests

# Configuración de la red WiFi
SSID = "Jorge"
PASSWORD = "12345"

# Token de acceso para la API de WhatsApp
TOKEN = "EAADGJZAYdRZBsBO1HQTyWG423FRj703ZBR9YUoFlz9f5G5sgcVKPVrtX85p7NA97GJ97j57ldPngt1ZBZAY32gvw4rdACWZAscTWcMainw3kvwIkiMYYGseEZAihxGgMtWqFz967ffeoeKr7qeamPTsW00xru2SSX0th9Llz1bRcCVS2AHckP3FgxaheRLrb62mcZBtm0uItwIw3xk1N"

# URL a donde se enviarán los mensajes de WhatsApp
SERVIDOR = "https://graph.facebook.com/v17.0/184761381381361/messages"

# Número de teléfono al que se enviará el mensaje
NUMERO_TELEFONO = "523333979218"

# JSON con el mensaje a enviar
payload = {
    "messaging_product": "whatsapp",
    "to": NUMERO_TELEFONO,
    "type": "text",
    "text": {"body": "Se ha abierto el Locker con el teclado"}
}

# Pines del teclado matricial
filas = [23, 22, 21, 19]
columnas = [18, 5, 17]

teclas = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

# Contraseña
contrasena_correcta = "123"
entrada_usuario = []

def conectar_wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("Conectado a la red WiFi")
    print("IP:", wlan.ifconfig()[0])

def leer_tecla():
    for i in range(3):
        machine.Pin(columnas[i], machine.Pin.OUT).value(1)
        for j in range(4):
            if machine.Pin(filas[j], machine.Pin.IN).value() == 0:
                return teclas[j][i]
        machine.Pin(columnas[i], machine.Pin.OUT).value(0)
    return None

def ingresar_contrasena():
    global entrada_usuario
    while True:
        tecla_presionada = leer_tecla()
        if tecla_presionada:
            entrada_usuario.append(tecla_presionada)
            print("Contraseña actual:", ''.join(entrada_usuario))
            time.sleep(0.2)  # Espera para evitar la repetición de teclas
        if len(entrada_usuario) == len(contrasena_correcta):
            break

def enviar_mensaje_whatsapp():
    if ''.join(entrada_usuario) == contrasena_correcta:
        print("Contraseña correcta. Enviando mensaje de WhatsApp...")
        
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
    entrada_usuario = []  # Reiniciar la entrada del usuario
    print("Por favor, ingrese la contraseña de 3 dígitos:")
    ingresar_contrasena()
    enviar_mensaje_whatsapp()
    time.sleep(1)  # Esperar 1 segundo antes de solicitar la contraseña nuevamente

