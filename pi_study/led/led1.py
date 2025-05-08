import RPi.GPIO as g
from time import sleep

ledPin = (16, 20, 21)

#BCM -> GPIO
#BOARD -> BOARD
g.setmode(g.BCM)
g.setup(ledPin, g.OUT)

try:
    while True:
        number = int(input("led number(1/2/3): "))
        mode = input("mode(on/off): ")
        if mode == "on":
            g.output(ledPin[number - 1], g.HIGH)
        elif mode == "off":
            g.output(ledPin[number - 1], g.LOW)
except KeyboardInterrupt:
    pass
finally:
    g.cleanup()