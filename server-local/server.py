#!/usr/bin/env python
import json

FILES_DIRECTORY = '/home/user/Desktop/selfie/pictures'

import os
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        self.generic_handler(False)

    def do_HEAD(self):
        """Serve a HEAD request."""
        self.generic_handler(True)

    def do_POST(self):
        """Serve a POST request."""
        r, info = self.handle_post()
        print r, info, "by: ", self.client_address
        f = StringIO()
        f.write('image uploaded successfully')
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self._copy_file(f, self.wfile)
            f.close()

    def handle_post(self):
        boundary = self.headers.plisttext.split("=")[1]
        remaining_bytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remaining_bytes -= len(line)
        if boundary not in line:
            return False, "Content NOT begin with boundary"
        line = self.rfile.readline()
        remaining_bytes -= len(line)
        file_name = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not file_name:
            return False, "Can't find out file name..."

        file_name = file_name[0]
        file_path = os.path.join(FILES_DIRECTORY, file_name)

        line = self.rfile.readline()
        if not line:
            remaining_bytes -= len(line)

        with open(file_path, 'wb') as out:
            preline = self.rfile.readline()
            remaining_bytes -= len(preline)
            while remaining_bytes > 0:
                line = self.rfile.readline()
                remaining_bytes -= len(line)
                if boundary in line:
                    preline = preline[0:-1]
                    if preline.endswith('\r'):
                        preline = preline[0:-1]
                    out.write(preline)
                    return True, "File '%s' upload success!" % file_name
                else:
                    out.write(preline)
                    preline = line
            return False, "Unexpect Ends of data."

    def generic_handler(self, metadata_only):
        path = os.path.join(FILES_DIRECTORY, self.path.strip('/'))
        if os.path.isdir(path):
            self.list_directory(path)
            return

        if not os.path.isfile(path):
            self.send_error(404, '{0} not found'.format(path))
            return

        file_type = self._guess_mime_type(path)
        with open(path, 'rb') as f:
            self.send_response(200)
            self.send_header("Content-type", file_type)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            if not metadata_only:
                self._copy_file(f, self.wfile)

    def list_directory(self, path):
        try:
            file_names = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        file_names.sort(key=lambda a: a.lower())
        f = StringIO()
        f.write(json.dumps(file_names))
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(length))
        self.end_headers()

        self._copy_file(f, self.wfile)

    def _copy_file(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

    def _guess_mime_type(self, path):
        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


def main(handler=SimpleHTTPRequestHandler, server=BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(handler, server)


if __name__ == '__main__':
    main()
