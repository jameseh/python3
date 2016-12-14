#!/usr/bin/env python
'''
Fetch the lastest APOD, pass if APOD is already in your library.
'''

import requests
import re
import os


PATH = '/home/james/Pictures/apod'
resp = requests.get('http://apod.nasa.gov/apod/').text
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
