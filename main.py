"""
Smart locket main program for the ESP32
"""
# programa copia locker
from machine import Pin, I2C
from kb4x4 import kb4x4
from i2c_lcd import I2cLcd
import time
import network
import socket
import utime
import machine


#Activar motor
def activar_motor(direccion1, direccion2, velocidad, tiempo):
    pin_direccion1.value(direccion1)
    pin_direccion2.value(direccion2)
    pin_activacion.on()
    time.sleep_ms(velocidad)
    pin_activacion.off()
    time.sleep(tiempo)  # Espera el tiempo adicional
    # Apaga el motor y regresa a la posición original
    pin_direccion1.value(not direccion1)
    pin_direccion2.value(not direccion2)
    pin_activacion.on()
    time.sleep_ms(velocidad)
    pin_activacion.off()

def on_pin_change(pin):
    if pin.value() == 1:
        lcd.clear()
        led.off()
        lcd.putstr("huella correcta")
        time.sleep(10)
        lcd.clear()
        lcd.putstr("Ingresa pin....:")
        # Activa el motor en una dirección (ajusta según tu configuración)
        activar_motor(1, 0, velocidad_motor, tiempo_giro)
        led.on()  # Apaga el LED después de activar el motor
    else:
        led.on()
        # Puedes apagar el motor cuando sea necesario

#programa server
            

def WiFi_connect(ssid, password, host_name):
    station = network.WLAN(network.STA_IF)
    station.active(True)
   # station.connect(ssid, password)
    station.config(dhcp_hostname=host_name)
    print("Connecting to WiFi ...")
    while not station.isconnected():
        utime.sleep(1)

    print('Connection successful: %s' % station.config('dhcp_hostname'))
    print(station.ifconfig())

# handle_request(conn, request_data, signal_value)
def handle_request(conn, request, signal_value):
    # Manejar la solicitud HTTP y enviar una respuesta básica
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + signal_value
    conn.send(response)
    print('Respuesta enviada.')
    time.sleep(1)
    if "open" in signal_value:
        abrir("Abierto desde la App")
    #else:
        
#abrimos cerraduras
def abrir(mensaje_acceso):
    lcd.clear()
    lcd.putstr(mensaje_acceso)
    led.off()
    time.sleep(4)
    # Activa el motor en una dirección (ajusta según tu configuración)
    activar_motor(0, 1, velocidad_motor, tiempo_giro)
    led.on()
    # Puedes apagar el motor aquí si es necesario

#cerramos cerraduras
def cerrar(mensaje_cierre):
    lcd.clear()
    lcd.putstr(mensaje_cierre)
    led.off()
    time.sleep(4)
    # Activa el motor en una dirección (ajusta según tu configuración)
    activar_motor(1, 0, velocidad_motor, tiempo_giro)
    led.on()
    # Puedes apagar el motor aquí si es necesario


# Inicialización de I2C
i2c = I2C(sda=Pin(21), scl=Pin(22))
lcd = I2cLcd(i2c, 0x27, 2, 16)
teclado = kb4x4()
led = Pin(13, Pin.OUT)  # Pin correcto
Led = Pin(12, Pin.OUT)  # Pin incorrecto
pin_entrada = Pin(14, Pin.IN)  # Nuevo pin de entrada
pin_activacion = Pin(25, Pin.OUT)  # Pin de activación del Puente H ENA
pin_direccion1 = Pin(26, Pin.OUT)  # Pin de dirección del motor 1 IN1
pin_direccion2 = Pin(27, Pin.OUT)  # Pin de dirección del motor 2 IN2

# Configuración de velocidad y dirección
velocidad_motor = 100  # Ajusta este valor según tus necesidades (puede variar de 0 a 100)
tiempo_giro = 20  # Tiempo en segundos para que el motor gire más

# Contraseña predefinida
contrasena_correcta = ['1', '2', '3']
ingresado = []
lcd.clear()
lcd.putstr("Bienvenido       Locker")
time.sleep(2)
lcd.clear()
lcd.putstr("Ingresa pin....:")
led.off()

# Configuración de la interrupción para el pin de entrada
pin_entrada.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=on_pin_change)

# Inicialización del server

# Configurar la conexión WiFi
ssid = 'Jorge'
password = '12345678'
host_name = 'locket'

WiFi_connect(ssid, password, host_name)

# Configurar el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 80))
server.listen(1)

print('Esperando conexión...')

# Establecer un temporizador para reiniciar el programa si no se recibe ningún dato en 10 segundos
timeout = 10  # segundos
last_data_time = utime.time()

while True:
    conn, addr = server.accept() #Espera señal del server
    #password = teclado.readkey() #Espera señal del teclado
#     if password:
#         if isinstance(password, tuple):
#             key = password[0]
#             lcd.putstr(str("*"))
# 
#             if key == "#":
#                 if ingresado == contrasena_correcta:
#                   abrir("Pin correcto")  
#                 else:
#                     lcd.clear()
#                     lcd.putstr("pin Incorrecto")
#                     Led.on()
#                     led.on()
#                     time.sleep(2)
#                     Led.off()
#                 lcd.clear()
#                 ingresado = []  # Reiniciar la lista para el nuevo intento
#                 lcd.putstr("Ingresa pin....:")
#                 
#             elif len(ingresado) < len(contrasena_correcta):
#                 ingresado.append(key)
# 
#             if len(ingresado) == len(contrasena_correcta):
#                 lcd.clear()
#                 lcd.putstr("pin ingresado:")
#                 lcd.move_to(0, 1)
#                 lcd.putstr("".join(map(str, " ")))
                
  #  else:
    print("Conexión establecida desde:", addr)

    # Reiniciar el temporizador cada vez que se recibe un dato
   # last_data_time = utime.time()

    # Recibir la solicitud HTTP
    request_data = conn.recv(2048).decode()
    print("Message")
    print(request_data) 

    # Buscar 'signal=' en la solicitud y extraer los siguientes 6 caracteres
    signal_index = request_data.find('signal=')
    if signal_index != -1:
        signal_value = request_data[signal_index + len('signal='):signal_index + len('signal=') + 6]

        # Limpiar la consola antes de imprimir la información sobre la señal
        print('\033c')  # Esto debería funcionar en muchos terminales

        # Imprimir la palabra clave encontrada después de 'signal='
        print('Signal value:', signal_value)
            

    # Manejar la solicitud y enviar la respuesta
    handle_request(conn, request_data, signal_value)

    # Cerrar la conexión
    conn.close()




