import RPi.GPIO as GPIO
import time

button_pin = 13  # 버튼이 연결된 핀

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(button_pin) == GPIO.LOW:
            print("Button Pressed!")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()

