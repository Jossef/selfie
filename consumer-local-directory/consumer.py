import requests
import os


def download_file(filename, path):
    url = 'http://jossef.com/selfie/uploads/{filename}'.format(filename=filename)
    r = requests.get(url, stream=True)
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def main():

    output_directory = os.path.expanduser("~/Desktop/selfie/pictures")
    url = 'http://jossef.com/selfie/uploads/'

    r = requests.get(url)

    file_names = r.json()

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    for file_name in file_names:
        path = os.path.join(output_directory, file_name)
        if os.path.exists(path):
            continue

        print 'downloading', file_name
        download_file(file_name, path)


main()
