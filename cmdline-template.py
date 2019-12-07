#!/usr/bin/env python3
"""
cmdline-template.py
python template to process command line files and folders
option to run recursively
"""

import argparse
import os
import errno
import subprocess


def which(program, required=True):
    ''' search for executable file '''
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    if required:
        print("Could not find required binary '{}'.".format(program))
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), program)

    return None


def process_file(filename):
    ''' process individual files. '''
    directory = os.path.split(filename)[0]
    file = os.path.split(filename)[1]
    ext = os.path.splitext(os.path.split(filename)[1])[1]

    if file == '.DS_Store':
        return

    # do the important stuff here
    call_list = ['ls', '-alp', filename]
    subprocess.call(call_list)


def process_dir(directory, recursive):
    ''' recursive into directories. '''
    for filename in os.listdir(directory):
        fullname = directory + '/' + filename
        #process_file(directory + '/' + filename)

        if os.path.isfile(fullname):
            process_file(fullname)

        if recursive and os.path.isdir(fullname):
            process_dir(fullname, recursive)


def main():
    ''' do the main thing '''
    parser = argparse.ArgumentParser(
        description='commandline file processor python template ')
    parser.add_argument("input", nargs='*',
                        default=None, help="accepts files and/or folders")
    parser.add_argument('-r', '--recursive', action='store_true', default=False,
                        dest='recursive', help='recurse into directories')

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return

    for single_input in args.input:
        if not (os.path.isdir(single_input) or os.path.isfile(single_input)):
            print('ERROR: input is not a file or a directory: ' + single_input)
            parser.print_help()
            return

        absinput = os.path.abspath(single_input)

        if os.path.isdir(absinput):
            process_dir(absinput, args.recursive)

        if os.path.isfile(absinput):
            process_file(absinput)

    return


if __name__ == "__main__":
    main()
