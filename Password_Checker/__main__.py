#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import argparse
from Password_Checker.modules import manage_file
from Password_Checker.modules import API_functions
from pathlib import Path
import getpass
import logging
import sys

# LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.INFO,
    filename=Path(__file__).parent / 'logs' / 'all_info_on.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(name)s -> %(funcName)s : %(message)s',
    encoding='utf-8')


# PROGRAM EXECUTION
def core_execution(
        passwords_list: list,
        verbosity: bool
) -> None:  # a function to slim the code in main()
    '''
    Parameters:
    - passwords_list : list - the list of passwords to check
    - sha_protocol : bool - the protocol to use
    '''

    if type(passwords_list) != list:
        print(
            'TypeError : the input is not a list, for more information check the log file')
        sys.exit()

    if len(passwords_list) <= 0:
        print('the list is empty, no passwords to check')
        sys.exit()

    else:
        sha_protocol = False  # when implemented & add a parameter to function
        count_records = []
        for password in passwords_list:
            count = API_functions.leaked_count(
                API_functions.pwned_API_check(password, sha256=sha_protocol))
            count_records.append(count)
            if count:
                print(f'\'{password}\' has been hacked {count} times')
            else:
                print(f'\'{password}\' is not been hacked')
        if (max(count_records) and verbosity):
            print('''For a better choise of your passwords, you can add some number and special caracters,
remember to always include both capital letter and lower letter, with at least of 8 characters.
                  ''')
    return None


def main():
    # PARSER CONFIGURATION
    parser = argparse.ArgumentParser(
        description='check the reliability of your passwords')

    sha256_protocol = parser.add_argument(
        '--sha256',
        help='unable to use the sha256 protocol, since not implemtented yet in the code functionalities',
        action='store_true')

    parser_verbosity = parser.add_argument(
        '-v', '--verbose',
        help='increase output verbosity',
        action='store_true')

    reading_mode = parser.add_mutually_exclusive_group(required=False)
    parser_pwcl = reading_mode.add_argument(
        '-fh', '--from_here',
        help='input the passwords here, following the command to get them',
        action='store_true')

    parser_example = reading_mode.add_argument(
        '-ex', '--example',
        help='use an example to show the program',
        action='store_true')

    parser_file = reading_mode.add_argument(
        '-fl', '--from_file',
        help='input the path to password\'s file, otherwise remember to fill the default file in your Desktop',
        default=manage_file.default_file_path(),
        type=Path)

    # ARGS PARSING
    args = parser.parse_args()

    sha_protocol = args.sha256
    if sha_protocol:
        logging.warning('not available yet, then checked using sha1 protocol')

    if args.example:
        core_execution(manage_file.txt_to_list(
            manage_file.example_file()), args.verbose)
        logging.info(
            'this is a fixed example no need to keep safe the passwords')
        sys.exit()

    elif args.from_here:
        passwords_list = getpass.getpass(
            prompt='insert the passwords here, separated by space (then ENTER): ').split()
        core_execution(passwords_list, args.verbose)
        logging.info('the passwords are not stored')
        sys.exit()

    elif args.from_file:  # It has to be at the end to avoid the execution of the default file
        the_file = Path(args.from_file)
        core_execution(manage_file.txt_to_list(the_file), args.verbose)
        manage_file.keep_passwords_safe(the_file)
        sys.exit()


if __name__ == '__main__':
    main()
