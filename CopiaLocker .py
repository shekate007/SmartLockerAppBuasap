from machine import Pin, I2C
from kb4x4 import kb4x4
from i2c_lcd import I2cLcd
import time

# Inicialización de I2C
i2c = I2C(sda=Pin(21), scl=Pin(22))
lcd = I2cLcd(i2c, 0x27, 2, 16)
teclado = kb4x4()
led = Pin(13, Pin.OUT)  # Pin correcto
Led = Pin(12, Pin.OUT)  # Pin incorrecto
pin_entrada = Pin(14, Pin.IN)  # Nuevo pin de entrada
pin_activacion = Pin(25, Pin.OUT)  # Pin de activación del Puente H ENA
pin_direccion1 = Pin(26, Pin.OUT)  # Pin de dirección del motor 1 IN1
pin_direccion2 = Pin(27 , Pin.OUT)  # Pin de dirección del motor 2 IN2

# Configuración de velocidad y dirección
velocidad_motor = 100  # Ajusta este valor según tus necesidades (puede variar de 0 a 100)
tiempo_giro = 10  # Tiempo en segundos para que el motor gire más

# Contraseña predefinida
contrasena_correcta = ['1', '2', '3']
ingresado = []
lcd.clear()
lcd.putstr("Bienvenido       Locker")
time.sleep(2)
lcd.clear()
lcd.putstr("Ingresa pin....:")

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
        led.on()
        lcd.putstr("huella correcta")
        time.sleep(10)
        lcd.clear()
        lcd.putstr("Ingresa pin....:")
        # Activa el motor en una dirección (ajusta según tu configuración)
        activar_motor(1, 0, velocidad_motor, tiempo_giro)
    else:
        led.off()
        # Puedes apagar el motor cuando sea necesario

# Configuración de la interrupción para el pin de entrada
pin_entrada.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=on_pin_change)

while True:
    # Código original para el teclado numérico y la lógica del pin 13
    password = teclado.readkey()
    if password:
        if isinstance(password, tuple):
            key = password[0]
            lcd.putstr(str("*"))

            if key == "#":
                if ingresado == contrasena_correcta:
                    lcd.clear()
                    lcd.putstr("pin Correcto")
                    led.on()
                    # Activa el motor en una dirección (ajusta según tu configuración)
                    activar_motor(1, 0, velocidad_motor, tiempo_giro)
                    led.off()
                    # Puedes apagar el motor aquí si es necesario
                else:
                    lcd.clear()
                    lcd.putstr("pin Incorrecto")
                    Led.on()
                    led.off()
                    time.sleep(2)
                    Led.off()
                lcd.clear()
                ingresado = []  # Reiniciar la lista para el nuevo intento
                lcd.putstr("Ingresa pin....:")

            elif len(ingresado) < len(contrasena_correcta):
                ingresado.append(key)

            if len(ingresado) == len(contrasena_correcta):
                lcd.clear()
                lcd.putstr("pin ingresado:")
                lcd.move_to(0, 1)
                lcd.putstr("".join(map(str, " ")))
