#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import argparse
from Password_Checker.modules import manage_file
from Password_Checker.modules.main_execution import core_execution
from pathlib import Path
import getpass
import logging
import sys
import os

# LOGGING CONFIGURATION
logging_file_path = os.path.join(os.getcwd(), 'all_info_on.log')

logging.basicConfig(
    level=logging.INFO,
    filename=Path(logging_file_path),
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(name)s -> %(funcName)s : %(message)s',
    encoding='utf-8')


def main():
    '''
    Here the configuration of the parsers and the different executions
    depending on parsers
    '''

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
            prompt='insert the passwords here, separated by this combination || (then ENTER): ').split(sep='||')
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
