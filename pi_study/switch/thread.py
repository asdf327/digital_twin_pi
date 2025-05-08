from threading import Thread
from time import sleep

def fx1():
    for i in range(10):
        print(f"fx1 - {i}")
        sleep(1)
        
def fx2():
    for i in range(10):
        print(f"fx2 - {i}")
        sleep(1)

if __name__ == "__main__":
    thesd1 = Thread(target=fx1, daemon=True)
    thesd2 = Thread(target=fx2, daemon=True)
    thesd1.start()
    thesd2.start()
    print("XX")