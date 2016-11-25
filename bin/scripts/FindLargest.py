#!/usr/bin/env python3
"""
Usage:   ./FindLargest.py [DIRECTORY PATH] [NUMBER OF FILES] [OPTIONAL] ...
Example: ./FindLargest.py /home 10 --pd=/dev,/sys,/proc --ere='^.+somepattern+.$'

Find all files in recursively from [DIRECTORY PATH], sort and display the [NUMBER OF FILES] specified.

Mandatory args:
[DIRECTORY]                                - Positional argument, full path of directory so search.
[NUMBER_OF_FILES]                          - Positional argument, number of files to display.

Optional args:
--pd                                       - Pass if directory starts with.
--pf                                       - Pass if file ends with.
--pdre                                     - Pass if directory matches regex.
--pfre                                     - Pass if file matches regex.
--mre                                      - Display only filenames or paths matching regex.
--ere                                      - Exclude all filenames or paths matching regex.
"""

import os
import sys
import argparse
import re


def main(path, number_of_items, pass_if_startswith=None, pass_if_endswith=None, pass_matching_directory_re=None,
         pass_matching_file_re=None, display_matching_re=None, exclude_matching_re=None):
    file_list = find_files(path, pass_if_startswith, pass_if_endswith, pass_matching_directory_re, pass_matching_file_re)
    file_list = sort_list(file_list)
    if not display_matching_re == None:
        file_list = show_only_matching_re(file_list, display_matching_re)
    elif not exclude_matching_re == None:
        file_list = show_exclude_matching_re(file_list, exclude_matching_re)
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


def format_pass_if(pass_if_startswith=None, pass_if_endswith=None):
    '''format optional arguement string into a tuple if it does not equal "None".'''
    if not pass_if_startswith == None:
        pass_if_startswith = pass_if_startswith.split(',')
        pass_if_startswith = tuple(pass_if_startswith)
        return pass_if_startswith
    elif not pass_if_endswith == None:
        pass_if_startswith = pass_if_endswith.split(',')
        pass_if_startswith = tuple(pass_if_endswith)
        return pass_if_endswith


def find_files(path, pass_if_startswith=None, pass_if_endswith=None, pass_matching_directory_re=None,
               pass_matching_file_re=None):
    '''find all files recursivly in a given path and save them in a list optionally ignoring
    directories specified.'''
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
        if pass_if_startswith == None and pass_if_endswith == None\
                and pass_matching_directory_re == None and pass_matching_file_re == None:
            for files in filenames:
                file_path = os.path.join(dirpath, files)
                if os.path.isfile(file_path):
                    file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None and not pass_if_endswith == None\
                and not pass_matching_directory_re == None and not pass_matching_file_re == None:
            if not dirpath.startswith(pass_if_startswith):
                if not re.search(pass_matching_directory_re, dirpath):
                    for files in filenames:
                        if not files.endswith(pass_if_endswith):
                            if not re.search(pass_matching_file_re, files):
                                file_path = os.path.join(dirpath, files)
                                if os.path.isfile(file_path):
                                    file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None and not pass_if_endswith == None and not pass_matching_directory_re == None:
            if not dirpath.startswith(pass_if_startswith):
                if not re.search(pass_matching_directory_re, dirpath):
                    for files in filenames:
                        if not filenames.endswith(pass_if_endswith):
                            file_path = os.path.join(dirpath, files)
                            if os.path.isfile(file_path):
                                file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None and not pass_if_endswith == None and not pass_matching_file_re == None:
            if not dirpath.startswith(pass_if_startswith):
                for files in filenames:
                    if not files.endswith(pass_if_endswith):
                        if not re.search(pass_matching_file_re, files):
                            file_path = os.path.join(dirpath, files)
                            if os.path.isfile(file_path):
                                file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None and not pass_matching_directory_re == None\
                and not pass_matching_file_re == None:
            if not re.search(pass_matching_directory_re, dirpath):
                if not dirpath.startswith(pass_if_startswith):
                    for files in filenames:
                        if not re.search(pass_matching_file_re, files):
                            file_path = os.path.join(dirpath, files)
                            if os.path.isfile(file_path):
                                file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_endswith == None and not pass_matching_directory_re == None\
                and not pass_matching_file_re == None:
            if not re.search(pass_matching_directory_re, dirpath):
                for files in filenames:
                    if not re.search(pass_matching_file_re, files):
                        if not files.endswith(pass_if_endswith):
                            file_path = os.path.join(dirpath, files)
                            if os.path.isfile(file_path):
                                file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None and not pass_if_endswith == None:
            if not dirpath.startswith(pass_if_startswith):
                for files in filenames:
                    if not files.endswith(pass_if_endswith):
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None and not pass_matching_directory_re == None:
            if not dirpath.startswith(pass_if_startswith):
                if not re.search(pass_matching_directory_re, dirpath):
                    for files in filenames:
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None and not pass_matching_file_re == None:
            if not dirpath.startswith(pass_if_startswith):
                for files in filenames:
                    if not re.search(pass_matching_file_re, files):
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_endswith == None and not pass_matching_directory_re == None:
            if not re.search(pass_matching_directory_re, dirpath):
                for files in filenames:
                    if not files.endswith(pass_if_endswith):
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_endswith == None and not pass_matching_file_re == None:
            for files in filenames:
                if not files.endswith(pass_if_endswith):
                    if not re.search(pass_matching_file_re, files):
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_matching_directory_re == None and not pass_matching_file_re == None:
            if not re.search(pass_matching_directory_re, dirpath):
                for files in filenames:
                    if not re.search(pass_matching_file_re, files):
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_startswith == None:
            if not dirpath.startswith(pass_if_startswith):
                for files in filenames:
                    file_path = os.path.join(dirpath, files)
                    if os.path.isfile(file_path):
                        file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_if_endswith == None:
            for files in filenames:
                if not files.endswith(pass_if_endswith):
                    file_path = os.path.join(dirpath, files)
                    if os.path.isfile(file_path):
                        file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_matching_directory_re == None:
            for files in filenames:
                for dirname in dirnames:
                    if not re.search(pass_matching_directory_re, dirname):
                        file_path = os.path.join(dirpath, files)
                        if os.path.isfile(file_path):
                            file_list.append((os.path.getsize(file_path), file_path))

        elif not pass_matching_file_re == None:
            for files in filenames:
                if not re.search(pass_matching_file_re, files):
                    file_path = os.path.join(dirpath, files)
                    if os.path.isfile(file_path):
                        file_list.append((os.path.getsize(file_path), file_path))
    return file_list


def sort_list(file_list):
    '''sort file_list, decending by size, in place.'''
    file_list.sort(reverse=True)
    return file_list


def show_exclude_matching_re(file_list, exclude_matching_re=None):
    '''exclude filenames and paths that match regex.'''
    if not exclude_matching_re == None:
        matching_list = []
        for size_in_bytes, name in file_list:
            if not re.search(exclude_matching_re, name):
                matching_list.append((size_in_bytes, name))
        file_list = matching_list
        return file_list


def show_only_matching_re(file_list, display_matching_re=None):
    if not display_matching_re == None:
        matching_list = []
        for size_in_bytes, name in file_list:
            if re.search(display_matching_re, name):
                matching_list.append((size_in_bytes, name))
        file_list = matching_list
        return file_list


def print_largest(file_list, number_of_items):
    '''print number_of_items of files and their size.'''
    for size_in_bytes, name in file_list[:number_of_items]:
        print("File: '{}' \nSize: {} \n".format(name, size(size_in_bytes)))


def check_regex_input(pass_matching_directory_re=None, display_matching_re=None, exclude_matching_re=None,
                      pass_matching_file_re=None):
    if not pass_matching_directory_re == None:
        try:
            assert re.compile(pass_matching_directory_re)
            return pass_matching_directory_re
        except:
            print('Enter a valid RE.')
    elif not display_matching_re == None:
        try:
            assert re.compile(display_matching_re)
            return display_matching_re
        except:
            print('Enter a valid RE.')
    elif not exclude_matching_re == None:
        try:
            assert re.compile(exclude_matching_re)
            return exclude_matching_re
        except:
            print('Enter a valid RE.')
    elif not pass_matching_file_re == None:
        try:
            assert re.compile(pass_matching_file_re)
            return pass_matching_file_re
        except:
            print('Enter a valid RE.')
    else:
        pass

if __name__ == '__main__':
    if len(sys.argv) < 3:
    #if user did not supply enough arguments, print the useage directions.
        print(__doc__)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("path", type=str, help="Path to search.")
        parser.add_argument("number_of_items", help="Number of files to display.")
        parser.add_argument("--pd", type=str, help="Pass if directory starts with.")
        parser.add_argument("--pf", type=str, help="Pass if file ends with.")
        parser.add_argument("--pdre", type=str, help="Pass if directory matches regex.")
        parser.add_argument("--pfre", type=str, help="Pass if file matches regex.")
        parser.add_argument("--mre", type=str, help="Display all files matching RE.")
        parser.add_argument("--ere", type=str, help="Exclude all files matching RE.")
        args = parser.parse_args()

        path = check_user_path(args.path)
        number_of_items = check_user_number(args.number_of_items)
        pass_if_startswith = format_pass_if(args.pd)
        pass_if_endswith = format_pass_if(args.pf)
        pass_matching_directory_re = check_regex_input(args.pdre)
        pass_matching_file_re = check_regex_input(args.pfre)
        display_matching_re = check_regex_input(args.mre)
        exclude_matching_re = check_regex_input(args.ere)

        main(path, number_of_items, pass_if_startswith, pass_if_endswith, pass_matching_directory_re,
             pass_matching_file_re, display_matching_re, exclude_matching_re)