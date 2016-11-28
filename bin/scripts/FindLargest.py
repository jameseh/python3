#!/usr/bin/env python3
"""
Usage:   ./FindLargest.py [DIRECTORY PATH] [NUMBER OF FILES] [OPTIONAL] ...
Example: ./FindLargest.py /home 10 --pd=/dev,/sys,/proc --ere='regex'

Find all files in recursively from [DIRECTORY PATH], sort and display the
[NUMBER OF FILES] specified.

Mandatory args:
[DIRECTORY]            - Positional argument, full path of directory so search.
[NUMBER_OF_FILES]      - Positional argument, number of files to display.

Optional args:
--mre                  - Display only filenames or paths matching regex.
--ere                  - Exclude all filenames or paths matching regex.

--pd                   - Pass if directory starts with.
--pf                   - Pass if file ends with.
--pdre                 - Pass if directory matches regex.
--pfre                 - Pass if file matches regex.

--sd                   - Search only in directories starting with.
--sf                   - Show only files ending with.
--sdre                 - Search only directories matching regex.
--sfre                 - Show only files matching regex.
"""


import os
import sys
import argparse
import re


def main(path, number_of_items, pass_if_startswith=None, pass_if_endswith=None,
         pass_matching_directory_re=None, pass_matching_file_re=None,
         display_matching_re=None, exclude_matching_re=None,
         display_if_startswith= None, display_if_endswith=None,
         display_matching_directory_re=None, display_matching_file_re=None):
    file_list = find_files(path, pass_if_startswith, pass_if_endswith,
                           pass_matching_directory_re, pass_matching_file_re,
                           display_if_startswith, display_if_endswith,
                           display_matching_directory_re,
                           display_matching_file_re)
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


def format_pass_if(pass_if_startswith=None, pass_if_endswith=None,
                   display_if_startswith=None, display_if_endswith= None):
    '''format optional arguement string into a tuple if not "None".'''
    if pass_if_startswith is not None:
        pass_if_startswith = pass_if_startswith.split(',')
        pass_if_startswith = tuple(pass_if_startswith)
        return pass_if_startswith
    if pass_if_endswith is not None:
        pass_if_startswith = pass_if_endswith.split(',')
        pass_if_startswith = tuple(pass_if_endswith)
        return pass_if_endswith
    if display_if_startswith is not None:
        display_if_startswith = display_if_startswith.split(',')
        display_if_startswith = tuple(display_if_startswith)
    if display_if_endswith is not None:
        display_if_endswith = display_if_endswith.split(',')
        display_if_endswith = tuple(display_if_endswith)


def find_files(path, pass_if_startswith=None, pass_if_endswith=None,
               pass_matching_directory_re=None,
               pass_matching_file_re=None, display_if_startswith=None,
               display_if_endswith=None, display_matching_directory_re=None,
               display_matching_file_re=None):
    '''find all files recursivly in a given path and save them in a list
    optionally ignoring directories specified.'''
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=False,
                                                followlinks=False):
        if pass_if_startswith is not None:
            if dirpath.startswith(pass_if_startswith):
                continue
        if pass_matching_directory_re is not None:
            if re.search(pass_matching_directory_re, dirpath):
                continue
        if display_if_startswith is not None:
            if not dirpath.startswith(display_if_startswith):
                continue
        if display_matching_directory_re is not None:
            if not re.search (display_matching_directory_re, dirpath):
                continue

        for files in filenames:
            if pass_if_endswith is not None:
                if files.endswith(pass_if_endswith):
                    continue
            if pass_matching_file_re is not None:
                if re.search(pass_matching_file_re, files):
                    continue
            if display_if_endswith is not None:
                if not files.endswith(display_if_endswith):
                    continue
            if display_matching_file_re is not None:
                if not re.search(display_matching_file_re, files):
                    continue

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
    if exclude_matching_re is not None:
        matching_list = []
        for size_in_bytes, name in file_list:
            if not re.search(exclude_matching_re, name):
                matching_list.append((size_in_bytes, name))
        file_list = matching_list
        return file_list


def show_only_matching_re(file_list, display_matching_re=None):
    '''show only filename and paths matching regex'''
    if display_matching_re is not None:
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


def check_regex_input(pass_matching_directory_re=None, display_matching_re=None
                      , exclude_matching_re=None, pass_matching_file_re=None,
                      display_matching_directory_re=None,
                      display_matching_file_re=None):
        try:
            if pass_matching_directory_re is not None:
                return re.compile(pass_matching_directory_re)
            if pass_matching_file_re is not None:
                return re.compile(pass_matching_file_re)
            if display_matching_re is not None:
                return re.compile(display_matching_re)
            if exclude_matching_re is not None:
                return re.compile(exclude_matching_re)
            if display_matching_directory_re is not None:
                return re.compile(display_matching_directory_re)
            if display_matching_file_re is not None:
                return re.compile(display_matching_file_re)
        except:
            print('Enter a valid RE.')


if __name__ == '__main__':
    if len(sys.argv) < 3:
    #if user did not supply enough arguments, print the useage directions.
        print(__doc__)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("path", type=str, help="Path to search.")
        parser.add_argument("number_of_items",
                            help="Number of files to display.")
        parser.add_argument("--pd", type=str,
                            help="Pass if directory starts with.")
        parser.add_argument("--pf", type=str, help="Pass if file ends with.")
        parser.add_argument("--pdre", type=str,
                            help="Pass if directory matches regex.")
        parser.add_argument("--pfre", type=str,
                            help="Pass if file matches regex.")

        parser.add_argument("--sd", type=str,
                            help="Search only in directories starting with.")
        parser.add_argument("--sf", type=str,
                            help="Show only files ending with.")
        parser.add_argument("--sdre", type=str,
                            help="Search only directories matching regex.")
        parser.add_argument("--sfre", type=str,
                            help="Show only files matching regex.")

        parser.add_argument("--mre", type=str,
                            help="Display all files matching"
                                                    " RE.")
        parser.add_argument("--ere", type=str,
                            help="Exclude all files matching"
                                                    " RE.")
        args = parser.parse_args()
        path = check_user_path(args.path)
        number_of_items = check_user_number(args.number_of_items)
        pass_if_startswith = format_pass_if(args.pd)
        pass_if_endswith = format_pass_if(args.pf)
        pass_matching_directory_re = check_regex_input(args.pdre)
        pass_matching_file_re = check_regex_input(args.pfre)
        display_matching_re = check_regex_input(args.mre)
        exclude_matching_re = check_regex_input(args.ere)
        display_if_startswith = format_pass_if(args.sd)
        display_if_endswith = format_pass_if(args.sf)
        display_matching_directory_re = check_regex_input(args.sdre)
        display_matching_file_re = check_regex_input(args.sfre)

        main(path, number_of_items, pass_if_startswith, pass_if_endswith,
             pass_matching_directory_re, pass_matching_file_re,
             display_matching_re, exclude_matching_re, display_if_startswith,
             display_if_endswith, display_matching_directory_re,
             display_matching_file_re)