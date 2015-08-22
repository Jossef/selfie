import time
from camera import Camera
import RPi.GPIO as GPIO
import requests
import logging
import sys
import ntpath

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()
pin = 7
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)


def upload_image(path):
    logging.debug('uploading {path}'.format(path=path))

    url = 'http://jossef.com/selfie/upload.php'
    filename = ntpath.basename(path)
    with open(path, 'rb') as f:
        files = {'file': (filename, f)}
        r = requests.post(url, files=files)
        r.raise_for_status()
        print r.text


def main():
    with Camera() as camera:
        GPIO.output(pin, GPIO.HIGH)
        image_path = camera.capture()
        #image_path = '/tmp/22-18-01-05.jpg'
        upload_image(image_path)
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
