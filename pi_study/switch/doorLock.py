import RPi.GPIO as GPIO
import time
import threading
from queue import Queue

class ButtonListener(threading.Thread):
    def __init__(self, index, pin, queue):
        super().__init__(daemon=True)
        self.index = index
        self.pin = pin
        self.queue = queue
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        print(f"ButtonListener {self.index} initialized.")  # Debugging output

    def run(self):
        while True:
            if GPIO.input(self.pin) == GPIO.LOW:
                print(f"Button {self.index + 1} pressed.")  # Confirm button press
                self.queue.put(self.index + 1)
                while GPIO.input(self.pin) == GPIO.LOW:
                    time.sleep(0.05)
                time.sleep(0.1)

class LEDController:
    def __init__(self, pins):
        self.pins = pins
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        print("LED Controller initialized.")  # Debugging output

    def success_pattern(self):
        print("Success pattern started.")  # Debugging output
        for _ in range(3):
            for pin in self.pins:
                GPIO.output(pin, True)
                time.sleep(0.3)
                GPIO.output(pin, False)
                time.sleep(0.2)
        print("Success pattern finished.")  # Debugging output

    def fail_pattern(self):
        print("Failure pattern started.")  # Debugging output
        for _ in range(3):
            for pin in self.pins:
                GPIO.output(pin, True)
            time.sleep(0.2)
            for pin in self.pins:
                GPIO.output(pin, False)
            time.sleep(0.2)
        print("Failure pattern finished.")  # Debugging output

class PasswordSystem:
    def __init__(self, button_pins, led_pins):
        self.queue = Queue()
        self.password = []
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        print("PasswordSystem initialization started.")  # Debugging output

        self.led = LEDController(led_pins)

        self.threads = [
            ButtonListener(i, pin, self.queue)
            for i, pin in enumerate(button_pins)
        ]
        for thread in self.threads:
            thread.start()

        print("PasswordSystem initialized.")  # Debugging output

    def set_password(self):
        print("🔐 Please set the password (between 111 and 333).")  # Debugging output
        while True:
            input_sequence = []
            while len(input_sequence) < 3:
                if not self.queue.empty():
                    value = self.queue.get()
                    print(f"Input: {value}")
                    input_sequence.append(value)

            pw_str = ''.join(str(d) for d in input_sequence)

            if self.is_valid_password(pw_str):
                self.password = input_sequence
                print(f"✅ Password set: {pw_str}")
                self.led.success_pattern()
                break
            else:
                print(f"❌ Password must be between '111' and '333'. Current input: {pw_str}")
                self.led.fail_pattern()

    def is_valid_password(self, pw_str):
        if len(pw_str) != 3 or not pw_str.isdigit():
            return False
        pw_int = int(pw_str)
        return 111 <= pw_int <= 333

    def run(self):
        self.set_password()
        try:
            while True:
                print("🔑 Please enter your password...")  # Debugging output
                input_sequence = []
                while len(input_sequence) < 3:
                    if not self.queue.empty():
                        value = self.queue.get()
                        print(f"Input: {value}")
                        input_sequence.append(value)

                if input_sequence == self.password:
                    print("✅ Password matched!")  # Debugging output
                    self.led.success_pattern()
                else:
                    print("❌ Password mismatch!")  # Debugging output
                    self.led.fail_pattern()

                time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting.")
        finally:
            GPIO.cleanup()
