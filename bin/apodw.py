#!/usr/bin/env python
'''
Download and set the the lastest APOD (Astronomy Picture of the Day) from
http://apod.nasa.gov, as wallpaper with feh, pass if the APOD is already in
library.
 '''


import requests
import re
import os
import sys
import time


def main():
    DIR_PATH = '/home/james/Pictures/apod/'  # path of the directory to search.
    resp = test_connection()
    file_list = create_file_list(DIR_PATH)

    if test_connection() is False:
        for count in range(0, 5):
            time.sleep(120)
            test_connection()
    else:
        download_apod(resp, DIR_PATH)
        create_file_list(DIR_PATH)
        create_file_list(DIR_PATH)
        set_background(file_list, DIR_PATH)


def test_connection():
    '''Test connection, return the response or 'False' if the request fails.'''
    try:
        resp = requests.get('http://apod.nasa.gov/apod/')
        return resp
    except requests.exceptions.ConnectionError:
        return False


def download_apod(resp, DIR_PATH):
    '''Check if APOD is in library, if not download todays APOD.'''
    resp = resp.text
    apod_suffix = re.search(r'(image/).*/(.*jpg)', resp).group()
    apod_url = '{}{}'.format('http://apod.nasa.gov/apod/', apod_suffix)
    file_name = os.path.split(apod_suffix)[1]

    # make sure we don't already have todays APOD.
    for dirpath, dirnames, filenames in os.walk(DIR_PATH, topdown=False,
                                                followlinks=False):
        if file_name in filenames:
            continue
        else:
            os.chdir(DIR_PATH)
            os.system('wget {}'.format(apod_url))
            os.system('touch -m {}'.format(file_name))


def create_file_list(DIR_PATH):
    '''Walk the DIR_PATH, find all files, add a tuple of st_mtime and the files
    name to a list.'''
    file_list = []
    for dirpath, dirnames, filenames in os.walk(DIR_PATH, topdown=False,
                                                followlinks=False):
        for files in filenames:
            file_path = os.path.join(dirpath, files)
            if os.path.isfile(file_path):
                file_list.append(
                    (os.stat(os.path.join(dirpath, files)).st_mtime, files))
    return file_list


def set_background(file_list, DIR_PATH):
    '''Set the most recently downloaded APOD to desktop wallpaper with feh.'''
    file_list.sort(reverse=True)
    background_path = '{}{}'.format(DIR_PATH, file_list[0][1])
    os.system('feh --bg-scale "{}"'.format(background_path))


if __name__ == '__main__':
    main()
