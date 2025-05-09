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

    def run(self):
        print("🔑 비밀번호를 입력하세요...")
        input_sequence = []
        while len(input_sequence) < 3:
            if not self.queue.empty():
                value = self.queue.get()
                print(f"입력: {value}")
                input_sequence.append(value)

        print(f"입력된 비밀번호: {input_sequence}")

class LEDController:
    def __init__(self, pins):
        self.pins = pins
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def success_pattern(self):
        for _ in range(3):
            for pin in self.pins:
                GPIO.output(pin, True)
                time.sleep(0.3)
                GPIO.output(pin, False)
                time.sleep(0.2)

    def fail_pattern(self):
        for _ in range(3):
            for pin in self.pins:
                GPIO.output(pin, True)
            time.sleep(0.2)
            for pin in self.pins:
                GPIO.output(pin, False)
            time.sleep(0.2)

class PasswordSystem:
    def __init__(self, button_pins, led_pins):
        self.queue = Queue()
        self.password = []
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.led = LEDController(led_pins)

        self.threads = [
            ButtonListener(i, pin, self.queue)
            for i, pin in enumerate(button_pins)
        ]
        for thread in self.threads:
            thread.start()

    def set_password(self):
        print("🔐 비밀번호를 설정하세요 (숫자 111~333 사이)")
        while True:
            input_sequence = []
            while len(input_sequence) < 3:
                if not self.queue.empty():
                    value = self.queue.get()
                    print(f"입력: {value}")
                    input_sequence.append(value)

            pw_str = ''.join(str(d) for d in input_sequence)

            if self.is_valid_password(pw_str):
                self.password = input_sequence
                print(f"✅ 비밀번호 설정 완료: {pw_str}")
                self.led.success_pattern()
                break
            else:
                print(f"❌ 비밀번호는 '111' 이상 '333' 이하 숫자여야 합니다. 현재 입력: {pw_str}")
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
                print("🔑 비밀번호를 입력하세요...")
                input_sequence = []
                while len(input_sequence) < 3:
                    if not self.queue.empty():
                        value = self.queue.get()
                        print(f"입력: {value}")
                        input_sequence.append(value)

                if input_sequence == self.password:
                    print("✅ 비밀번호 일치!")
                    self.led.success_pattern()
                else:
                    print("❌ 비밀번호 불일치!")
                    self.led.fail_pattern()

                time.sleep(1)
        except KeyboardInterrupt:
            print("종료합니다.")
        finally:
            GPIO.cleanup()

