#!/usr/bin/env python
'''
Fetch the lastest APOD, pass if APOD is already in your library.
'''


import requests
import re
import os
import time


def main():
    PATH = '/home/james/Pictures/apod'
    resp = test_connection()

    if test_connection() is not False:
        download_set(resp, PATH)
    if test_connection() is False:
        for count in range(6):
            time.sleep(60)
            test_connection()


def test_connection():
    try:
        resp = requests.get('http://apod.nasa.gov/apod/')
        return resp
    except requests.exceptions.ConnectionError:
        return False


def download_set(resp, PATH):
    resp = resp.text
    apod_suffix = re.search(r'(image/).*/(.*jpg)', resp).group()
    apod_url = '{}{}'.format('http://apod.nasa.gov/apod/', apod_suffix)
    file_name = os.path.split(apod_suffix)[1]

    for dirpath, dirnames, filenames in os.walk(PATH, topdown=False, followlinks=False):
        if file_name in filenames:
            continue
        else:
            os.chdir(PATH)
            os.system('wget {}'.format(apod_url))
            os.system('touch -m {}'.format(file_name)) # change st-mtime to current time.


if __name__ == '__main__':
    main()