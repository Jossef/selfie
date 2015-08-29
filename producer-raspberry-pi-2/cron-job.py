import ntpath
import time
import logging
import sys

from serial import Serial
import requests

sys.path.insert(0, '..')
from camera import Camera

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

# -------------

ARDUINO_SERIAL_PORT = '/dev/ttyACM0'
SECONDS = 30
UPLOAD_URL = 'http://10.0.0.9:8000'
# UPLOAD_URL = 'http://jossef.com/selfie/upload.php'


# -------------


def upload_image(path):
    logging.debug('uploading {path}'.format(path=path))

    filename = ntpath.basename(path)
    with open(path, 'rb') as f:
        files = {'file': (filename, f)}
        r = requests.post(UPLOAD_URL, files=files)
        r.raise_for_status()
        logging.debug('this is the upload response - {0}'.format(r.text))


def countdown(seconds):
    seconds = str(seconds)
    logging.debug('writing to Arduino the using a serial with the countdown of {0} seconds'.format(seconds))

    with Serial(ARDUINO_SERIAL_PORT, 9600) as s:
        s.write(seconds)


def capture_using_camera():
    with Camera() as camera:
        image_path = camera.capture()
        return image_path


def main():
    countdown(SECONDS)
    time.sleep(SECONDS + 3)  # Adding some grace
    image_path = capture_using_camera()
    upload_image(image_path)


def _exit():
    pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        _exit()
