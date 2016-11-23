#!/usr/bin/env python3

"""Find all files in path, display specified amount of the largest files and thier size.
Usage:   ./FindLargest.py [path] [number-of-files-to-display] Optional(--ps=[paths,to,exclude])
Example: ./FindLargest.py /home 10 --ps=/dev,/sys,/proc
"""

import os
import sys
import argparse


def main(path, number_of_items, pass_if_startswith=None):
    file_list = find_files(path, pass_if_startswith)
    file_list = sort_list(file_list)
    print_largest(file_list, number_of_items)


def size(num, suffix='B'):
    '''convert bytes to human'''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def check_user_number(number_of_items):
    '''make sure number_of_items is a valid path.'''
    try:
        number_of_items = int(number_of_items)
        assert number_of_items > 0
        return number_of_items
    except ValueError:
        print('Please enter a positive integer.')
    except AssertionError:
        print('Please enter a number of items greater than 0')
    sys.exit(1)


def check_user_path(path):
    '''make sure path is a valid directory.'''
    try:
        assert os.path.isdir(path)
        return path
    except AssertionError:
        print('Please enter a valid path')
    sys.exit(1)


def format_pass_if_startswith(pass_if_startswith=None):
    '''format optional arguement string into a tuple if it does not equal "None".'''
    if pass_if_startswith == None:
        return pass_if_startswith
    else:
        pass_if_startswith = pass_if_startswith.split(',')
        pass_if_startswith = tuple(pass_if_startswith)
        return pass_if_startswith


def find_files(path, pass_if_startswith=None):
    '''find all files recursivly in a given path and save them in a list optionally ignoring
    directories specified.'''
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
        if not pass_if_startswith == None:
            if not dirpath.startswith(pass_if_startswith):
                for files in filenames:
                    file_path = os.path.join(dirpath, files)
                    if os.path.isfile(file_path):
                        file_list.append((os.path.getsize(file_path), file_path))
        else:
            for files in filenames:
                file_path = os.path.join(dirpath, files)
                if os.path.isfile(file_path):
                    file_list.append((os.path.getsize(file_path), file_path))
    return file_list


def sort_list(file_list):
    '''sort file_list, decending by size, in place.'''
    file_list.sort(reverse=True)
    return file_list


def print_largest(file_list, number_of_items):
    '''print number_of_items of files and their size.'''
    for size_in_bytes, name in file_list[:number_of_items]:
        print("File: '{}' \nSize: {} \n".format(name, size(size_in_bytes)))


if __name__ == '__main__':
    if len(sys.argv) < 3:
    #if user did not supply enough arguments, print the useage directions.
        print(__doc__)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ps", type=str, help="Pass if directory starts with.")
        parser.add_argument("path", type=str, help="Path to search.")
        parser.add_argument("number_of_items", help="Number of files to display.")
        args = parser.parse_args()

        pass_if_startswith = format_pass_if_startswith(args.ps)
        path = check_user_path(args.path)
        number_of_items = check_user_number(args.number_of_items)

        main(path, number_of_items, pass_if_startswith)