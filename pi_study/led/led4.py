import RPi.GPIO as g
from time import sleep

ledPin = (16, 21)

g.setmode(g.BCM)
for pin in ledPin:
  g.setup(ledPin, g.OUT)

currentPassword = None

while True:
  newPassword = input("confirm passwor:")
  confirmPassword = input("new passwor: ")
  if newPassword == confirmPassword:
      currentPassword = newPassword
      print("O")
      break
  else:
      print("X")

while True:
  loginPassword = input("iogin password")
  if loginPassword == currentPassword:
      g.output(16, g.HIGH)
      break
  else:
      for i in range(5):
        g.output(21, g.HIGH)
        sleep(0.1)
        g.output(21, g.LOW)
        sleep(0.1)
    