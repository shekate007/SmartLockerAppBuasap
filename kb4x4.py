"""
example
kb = kb4x4()
letter, is_long = kb.readkey()
wiring:
        <..cols..>  <..rows...>
keypad: 1  2  3  4  5  6  7  8
esp:    16 15 10 12 13 0  2  14
"""

from time import sleep_ms, ticks_ms
import machine


class kb4x4:

    LONG_TIME = 300
    ACTIVE = 0
    PASSIVE = 1

    default_keyfield = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']]

    default_colPIN = [15, 2, 4, 16] #columnas 5 - 8
    default_rowPIN = [17, 5, 18, 19]  #Filas 1 - 4
 
    def __init__(self,
                 colPIN=default_colPIN,
                 rowPIN=default_rowPIN,
                 keyfield=default_keyfield):
        self.keyfield = keyfield
        self.colPIN = colPIN
        self.rowPIN = rowPIN
        self.COLS = len(self.colPIN)
        self.ROWS = len(self.rowPIN)
        self.col = []
        self.row = []
        for i in range(self.COLS):
            self.col.insert(i, machine.Pin(self.colPIN[i], machine.Pin.OUT))
            self.row.insert(i, machine.Pin(self.rowPIN[i],
                            machine.Pin.IN, machine.Pin.PULL_UP))

    def readkey(self):
        while True:
            for i in range(self.COLS):
                self.col[i].value(self.ACTIVE)
                self.col[(i - 1) % self.COLS].value(self.PASSIVE)
                for j in range(self.ROWS):
                    if self.row[j].value() == 0:
                        timer = ticks_ms()
                        while self.row[j].value() == 0:
                            pass
                        if ticks_ms() - timer > self.LONG_TIME:
                            return self.keyfield[i][j], True
                        return self.keyfield[i][j], False
            sleep_ms(50)
    