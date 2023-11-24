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

# Contraseña predefinida
contrasena_correcta = ['1', '2', '3']
ingresado = []
lcd.clear()
lcd.putstr("Bienvenido       Locker")
time.sleep(2)
lcd.clear()
lcd.putstr("Ingresa pin....:")

def on_pin_change(pin):
    if pin.value() == 1:
        lcd.clear()
        led.on()
        lcd.putstr("huella correcta")
        time.sleep(10)
        lcd.clear()
        lcd.putstr("Ingresa pin....:")
    else:
        led.off()

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
                    Led.off()
                    time.sleep(10)
                    led.off()
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
