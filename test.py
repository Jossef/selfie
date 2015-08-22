import time
from camera import Camera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
pin = 7
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)


def main():
    with Camera() as camera:
        GPIO.output(pin, GPIO.HIGH)
        camera.capture()
        GPIO.output(pin, GPIO.LOW)


def exit():
    GPIO.cleanup()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit()
