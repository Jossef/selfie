import os
from datetime import datetime
import gphoto2 as gp
import time
import logging


def ordinal(n):
    return str(n) + ('th' if 4 <= n <= 20 or 24 <= n <= 30 else ['st', 'nd', 'rd'][n % 10 - 1])


class Camera(object):
    def __init__(self):
        self._context = None
        self._camera = None

    @staticmethod
    def close_other_gphoto_processes():
        logging.debug('closing other opened gphoto processes (using pkill)')
        os.system('pkill -9 gphoto -f')

    def connect(self):

        if self._camera is not None and self._context is not None:
            logging.warn('asked to connect over an opened connection, ignoring')
            return

        self.close_other_gphoto_processes()

        success = False
        tries = 1

        while not success:
            try:
                logging.debug('trying to open a connection')
                self._camera = gp.check_result(gp.gp_camera_new())
                self._context = gp.gp_context_new()
                success = True
            except Exception as ex:
                logging.debug('failed to open a connection', exc_info=True)
                if tries > 5:
                    raise ex
                tries += 1
                time.sleep(0.5)

        logging.debug('opened a new connection')
        return self

    def disconnect(self):
        logging.debug('trying to close an existing connection')

        if self._camera is not None and self._context is not None:
            gp.gp_camera_exit(self._camera, self._context)

        self._camera = None
        self._context = None
        self.close_other_gphoto_processes()

    def __enter__(self):
        return self.connect()

    def __exit__(self, type, value, traceback):
        return self.disconnect()

    def list_files(self, path='/'):
        self._ensure_has_open_connection()
        logging.debug('listing files')

        result = []
        # get files
        for name, value in gp.check_result(
                gp.gp_camera_folder_list_files(self._camera, path, self._context)):
            yield path, name
        # read folders
        folders = []
        for name, value in gp.check_result(
                gp.gp_camera_folder_list_folders(self._camera, path, self._context)):
            folders.append(name)
        # recurse over subfolders
        for name in folders:
            for item in self.list_files(os.path.join(path, name)):
                yield item

    def capture(self, output_directory='/tmp'):

        if not os.path.isdir(output_directory):
            logging.debug("output directory {0} does not exists on disk, let's create it".format(output_directory))
            os.makedirs(output_directory)

        self._ensure_has_open_connection()
        logging.debug('capturing an image')

        tries = 1
        while True:
            try:
                logging.debug('{0} attempt to capture an image'.format(ordinal(tries)))

                destination_file_path = self._capture_attempt(output_directory)
                logging.debug('image downloaded successfully')
                return destination_file_path

            except Exception as ex:
                if isinstance(ex, gp.GPhoto2Error):
                    if ex.code == -105:
                        logging.warn('maybe the camera went offline?')

                logging.debug('failed to capture an image', exc_info=True)
                if tries >= 3:
                    raise ex
                tries += 1
                time.sleep(0.5)

    def _capture_attempt(self, output_directory):
        file_path = gp.check_result(gp.gp_camera_capture(self._camera, gp.GP_CAPTURE_IMAGE, self._context))
        logging.debug('camera file path: {0}{1}'.format(file_path.folder, file_path.name))
        destination_file_name = datetime.now().strftime('%d-%H-%M-%S.jpg')
        destination_file_path = os.path.join(output_directory, destination_file_name)
        logging.debug('downloading image to {0}'.format(destination_file_path))
        camera_file = gp.check_result(gp.gp_camera_file_get(self._camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL, self._context))
        gp.check_result(gp.gp_file_save(camera_file, destination_file_path))
        return destination_file_path

    def _ensure_has_open_connection(self):
        if self._camera is None or self._context is None:
            raise Exception('sorry, connection must be opened before using this function')
