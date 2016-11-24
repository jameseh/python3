#!/usr/bin/env python3

"""Find all files in path, display specified amount of the largest files and thier size.
Usage:   ./FindLargest.py [path] [number-of-files-to-display] Optional(--psw=[paths,to,exclude]
Optional(--ere='regualar expression to exclude')
Example: ./FindLargest.py /home 10 --psw=/dev,/sys,/proc --ere='^.*\.txt$'
"""

import os
import sys
import argparse
import re

def main(path, number_of_items, pass_if_startswith=None, pass_matching_directory_re=None, display_matching_re=None):
    file_list = find_files(path, pass_if_startswith, pass_matching_directory_re)
    file_list = sort_list(file_list)
    check_regex_input(pass_matching_directory_re, display_matching_re)
    print_largest(file_list, number_of_items)


def size(num, suffix='B'):
    '''convert bytes to human'''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "{:3.1f}{}{}".format(num, unit, suffix)
        num /= 1024.0
    return "{:.1f}{}{}".format(num, 'Yi', suffix)


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


def find_files(path, pass_if_startswith=None, pass_matching_directory_re=None):
    '''find all files recursivly in a given path and save them in a list optionally ignoring
    directories specified.'''
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
        if pass_if_startswith == None and pass_matching_directory_re == None:
            for files in filenames:
                file_path = os.path.join(dirpath, files)
                if os.path.isfile(file_path):
                    file_list.append((os.path.getsize(file_path), file_path))
        elif not pass_if_startswith == None and not pass_matching_directory_re == None:
            if not dirpath.startswith(pass_if_startswith):
                if re.search(pass_matching_directory_re, dirpath):
                    pass
                else:
                    for files in filenames:
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))
        elif not pass_if_startswith == None:
            if not dirpath.startswith(pass_if_startswith):
                for files in filenames:
                    file_path = os.path.join(dirpath, files)
                    if os.path.isfile(file_path):
                        file_list.append((os.path.getsize(file_path), file_path))
        elif not pass_matching_directory_re == None:
            if re.search(pass_matching_directory_re, dirpath):
                pass
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


def show_only_matching_re(file_list, display_matching_re=None):
    if not display_matching_re == None:
        file_list = filter(display_matching_re.search, file_list)
    return file_list


def print_largest(file_list, number_of_items):
    '''print number_of_items of files and their size.'''
    for size_in_bytes, name in file_list[:number_of_items]:
        print("File: '{}' \nSize: {} \n".format(name, size(size_in_bytes)))


def check_regex_input(pass_matching_directory_re=None, display_matching_re=None):
    if not pass_matching_directory_re == None:
        try:
            pass_matching_directory_re = re.compile(pass_matching_directory_re)
        except:
            print('Enter a valid RE.')
    if not display_matching_re == None:
        try:
            display_matching_re = re.compile(display_matching_re)
        except:
            print('Enter a valid RE.')
    return pass_matching_directory_re and display_matching_re


if __name__ == '__main__':
    if len(sys.argv) < 3:
    #if user did not supply enough arguments, print the useage directions.
        print(__doc__)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--psw", type=str, help="Pass if directory starts with.")
        parser.add_argument("--pre", type=str, help="Pass if directory contains RE.")
        parser.add_argument("--mre", type=str, help="Display all files matching RE.")
        parser.add_argument("path", type=str, help="Path to search.")
        parser.add_argument("number_of_items", help="Number of files to display.")
        args = parser.parse_args()

        pass_if_startswith = format_pass_if_startswith(args.psw)
        path = check_user_path(args.path)
        pass_matching_directory_re = check_regex_input(args.pre)
        display_matching_re = check_regex_input(args.mre)
        number_of_items = check_user_number(args.number_of_items)

        main(path, number_of_items, pass_if_startswith, pass_matching_directory_re, display_matching_re)