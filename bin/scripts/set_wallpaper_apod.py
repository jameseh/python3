#!/usr/bin/env python

'''Set background with most recent APOD, .'''

import os
import time


PATH = '/home/james/Pictures/apod/' # path of the directory to search.
SLEEP = 3600

def main(path):
    file_list = create_file_list(path)
    set_background(file_list)


def create_file_list(path):
    '''Walk the PATH, find all files and add a tuple of st_mtime and the files
    name to a list.'''
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
        for files in filenames:
            file_path = os.path.join(dirpath, files)
            if os.path.isfile(file_path):
                file_list.append((os.stat(os.path.join(dirpath, files)).st_mtime, files))
    return file_list


def set_background(file_list):
    '''Get most recently downloaded apod and set it to wallpaper.'''
    file_list.sort(reverse=True)
    background_path = '{}{}'.format(PATH, file_list[0][1])
    os.system('feh --bg-scale "{}"'.format(background_path))
    print(background_path)


if __name__ == '__main__':
    while True:
        main(PATH)
        time.sleep(SLEEP)
