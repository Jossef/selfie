import ntpath
import time
import requests


def upload_image(path):
    url = 'http://10.0.0.9:8000/'
    filename = ntpath.basename(path)
    with open(path, 'rb') as f:
        files = {'file': (filename, f)}
        r = requests.post(url, files=files)
        r.raise_for_status()


def main():
    upload_image('/home/user/Desktop/selfie/29-10-00-04.jpg')


def exit():
    pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit()
