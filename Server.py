import network
import socket
import utime
import machine

def WiFi_connect(ssid, password, host_name):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    station.config(dhcp_hostname=host_name)
    print("Connecting to WiFi ...")
    while not station.isconnected():
        utime.sleep(1)

    print('Connection successful: %s' % station.config('dhcp_hostname'))
    print(station.ifconfig())

def handle_request(conn, request):
    # Manejar la solicitud HTTP y enviar una respuesta básica
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello, this is a MicroPython Web Server!</h1>"
    conn.send(response)
    print('Respuesta enviada.')

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
    conn, addr = server.accept()
    print('Conexión establecida desde:', addr)

    # Reiniciar el temporizador cada vez que se recibe un dato
    last_data_time = utime.time()

    # Recibir la solicitud HTTP
    request_data = conn.recv(1024).decode()

    # Buscar 'signal=' en la solicitud y extraer los siguientes 6 caracteres
    signal_index = request_data.find('signal=')
    if signal_index != -1:
        signal_value = request_data[signal_index + len('signal='):signal_index + len('signal=') + 6]

        # Limpiar la consola antes de imprimir la información sobre la señal
        print('\033c')  # Esto debería funcionar en muchos terminales

        print('Signal value:', signal_value)

    # Manejar la solicitud y enviar la respuesta
    handle_request(conn, request_data)

    # Cerrar la conexión
    conn.close()

    # Verificar si ha pasado el tiempo de espera sin recibir datos y reiniciar el programa
    if utime.time() - last_data_time > timeout:
        print(f"No se recibieron datos en {timeout} segundos. Reiniciando el programa.")
        machine.reset()
