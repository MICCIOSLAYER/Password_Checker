#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import argparse
from Password_Checker.modules import manage_file 
from Password_Checker.modules import API_functions 
from Password_Checker.modules import Textuals 
import pathlib
import os
from pathlib import Path
import getpass
import logging
import sys

#LOGGING CONFIGURATION
logging.basicConfig(
    level=logging.DEBUG, 
    filename='main_log.log',
    filemode='w', 
    format='%(asctime)s - %(levelname)s - %(message)s', 
    encoding='utf-8')

# PROGRAM EXECUTION 2.0
def core_execution(
        passwords_list : list, 
        sha_protocol : bool
        )-> None: # a function to slim the code in main()
    '''
    Parameters:
    - passwords_list : list - the list of passwords to check
    - sha_protocol : bool - the protocol to use
    '''
    
    if type(passwords_list) != list:
        print('TypeError : the input is not a list, for more information check the main_log.log file')
        sys.exit()
    
    if len(passwords_list) <= 0:
        print('the list is empty, no passwords to check')
        sys.exit()

    else:
        sha_protocol = False # when implemented use remove this line
        for password in passwords_list:
            count = API_functions.conta_trapelate(API_functions.pwned_API_check(password, sha256=sha_protocol))
            if count:
                print(f'\'{password}\' has been hacked {count} times')
            else:
                print(f'\'{password}\' is not been hacked')
    return None




def main():
    logging.basicConfig(filename='mainlog.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(name)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%D %H:%M:%S')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='check the reliability of your passwords')

    sha256_protocol = parser.add_argument(
        '--sha256', 
        help='unable to use the sha256 protocol, since not implemtented yet in the code functionalities', 
        action='store_true') 


    reading_mode = parser.add_mutually_exclusive_group(required=False) 
    parser_pwcl = reading_mode.add_argument(
        '-fh', '--from_here', 
        help='input the passwords here, following the command to get them', 
        action='store_true') 
    
    parser_example = reading_mode.add_argument(
        '-ex', '--example', 
        help='use an example to show the program', 
        action='store_true', 
        default=False)
    
    parser_file = reading_mode.add_argument(
        '-fl', '--from_file', 
        help='input the path to password\'s file, otherwise remember to fill the default file in your Desktop', 
        default=manage_file.default_file_path(), 
        type=Path) 
    
    verification_parser = reading_mode.add_argument(# TODO remove once test on it are finished
        '-v', '--verify', 
        help='analyze and testing', 
        type=Path, 
        default=None) 

    args =  parser.parse_args()
    logging.debug(f'\nargs: {args} \n')
    logging.debug(f'\nargs.verify: {args.verify} \nargs.example: {args.example}  \nargs.from_here: {args.from_here} \nargs.sha256: {args.sha256}\nargs.from_file: {args.from_file}')
    
    sha_protocol = args.sha256
    if sha_protocol: 
        logging.warning('not available yet, then checked using sha1 protocol')
        


    if args.example:
        core_execution(manage_file.txt_to_list(manage_file.example_file()), sha_protocol)
        logging.info('this is a fixed example no need to keep safe the passwords')
        sys.exit() 

    elif args.from_here: 
        passwords_list = getpass.getpass(prompt='insert the passwords here, separated by space (then ENTER): ').split()
        core_execution(passwords_list, sha_protocol)
        logging.debug(f'the passwords_list is a type: {type(passwords_list)}')
        sys.exit()
        

    # TODO remove once test on it are finished
    elif args.verify: # continua a testare, -> testa il default path execution  per scrivere un contenuto aggiuntivo 
        print(f'all\'interno di args.verify vi è assegnato il valore : {args.verify} ')
        sys.exit() #FIXED?


    elif args.from_file:  #  It has to be at the end to avoid the execution of the default file 
        the_file = Path(args.from_file)
        core_execution(manage_file.txt_to_list(the_file), sha_protocol) # when implemented use sha_protocol
        manage_file.keep_passwords_safe(the_file)
        sys.exit() 

if __name__ == '__main__':
    main()
    
    

        