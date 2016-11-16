#!/usr/bin/env python3
import os
import sys
'''Find all files in path, display number of the largest files.
   Example: ./FindLargest.py /home/ 50'''


FILE_LIST = []
SORTED_LIST = []
PATH = sys.argv[1]
NUMBER_OF_ITEMS = sys.argv[2]


def main():
    check_user_input(PATH, NUMBER_OF_ITEMS)
    find_files(PATH)
    sort_list(FILE_LIST)
    print_largest(SORTED_LIST, NUMBER_OF_ITEMS)


def size(num, suffix='B'):
#convert bytes to human
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def check_user_input(PATH, NUMBER_OF_ITEMS):
#make sure PATH and NUMBER_OF_ITEMS are valid inputs
    try:
        NUMBER_OF_ITEMS = int(NUMBER_OF_ITEMS)
        if not os.path.isdir(PATH) is True:
            print('Please enter a valid path.')
        if float(NUMBER_OF_ITEMS) < 0:
            quit()
    except:
        print('Please enter a positive integer.')
        quit()


def find_files(PATH):
#find all files recursivly in a given path and save them in a list
    for dirpath, dirnames, filenames in os.walk(PATH, topdown=False, followlinks=False):
        if not dirpath.startswith(('/proc', '/dev', '/sys', '/run')):
            for files in filenames:
                file_path = os.path.join(dirpath, files)
                if os.path.isfile(file_path) == True:
                    FILE_LIST.append((os.path.getsize(file_path), file_path))


def sort_list(FILE_LIST):
    global SORTED_LIST
    SORTED_LIST = sorted(FILE_LIST, reverse=True)


def print_largest(SORTED_LIST, NUMBER_OF_ITEMS):
#print NUMBER_OF_ITEMS of files and their size.
    for items in SORTED_LIST[:int(NUMBER_OF_ITEMS)]:
        print("File: '%s' \nSize: %s \n" % (items[1], size(items[0])))


if __name__ == '__main__':
    main()