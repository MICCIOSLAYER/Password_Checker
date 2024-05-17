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

logging.basicConfig(level=logging.DEBUG, filename='log.log',filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# ESECUZIONE DEL PROGRAMMA 2.0
def core_execution(passwords_list : list, sha_protocol : bool)-> None: # a function to slim the code in main()
    '''
    Parameters:
    - passwords_list : list - the list of passwords to check
    - sha_protocol : bool - the protocol to use
    '''
    # 
    if len(passwords_list) <= 0:
        print('the list is empty, no passwords to check')
    else:
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
                        format='%(asctime)s %(levelname)-8s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%D %H:%M:%S')
 
    parser = argparse.ArgumentParser(description='check the reliability of your passwords')
    sha256_protocol = parser.add_argument('--sha256', help='unable to use the sha256 protocol, since not implemtented yet in the code functionalities', action='store_true') # FIXME use a False default value

    reading_mode = parser.add_mutually_exclusive_group(required=False) 
    parser_pwcl = reading_mode.add_argument('-fh', '--from_here', help='input the passwords here, following the command to get them', action='store_true') 
    parser_example = reading_mode.add_argument('-ex', '--example', help='use an example to show the program', action='store_true', default=False)
    parser_file = reading_mode.add_argument('-fl', '--from_file', help='input the path to password\'s file, otherwise remember to fill the default file in your Desktop', default=manage_file.default_file_path(), type=Path) 
    verification_parser = reading_mode.add_argument('-v', '--verify', help='analyze and testing', type=Path, default=None) # TODO remove once test on it are finished

    args =  parser.parse_args()
    logging.info(f'\nargs: {args} \n')
    logging.info(f'args.verify: {args.verify} \nargs.example: {args.example} \nargs.from_file: {args.from_file} \nargs.from_here: {args.from_here} \nargs.sha256: {args.sha256}\n')
    sha_protocol = args.sha256
    if sha_protocol: 
        logging.warning('this option is not available yet, then the passwords will be checked with sha1 protocol')
        sha_protocol = False  


    if args.example:
        example_path = manage_file.example_file() #HACK after testing replace the path with a simple list of strings
        core_execution(manage_file.txt_to_list(example_path), sha_protocol)
        logging.info('since this is an example, the passwords are casual and to be cancelled by the real file once the code is ok')
        sys.exit() 

    elif args.from_here: 
        passwords_list = getpass.getpass(prompt='insert the passwords here, separated by space (then ENTER): ').split()
        core_execution(passwords_list, sha_protocol)
        sys.exit()
        

    # TODO remove once test on it are finished
    elif args.verify: # continua a testare, -> testa il default path execution  per scrivere un contenuto aggiuntivo 
        print(f'all\'interno di args.verify vi è assegnato il valore : {args.verify} ')
        sys.exit() #FIXED?

    #it has to be at the end to avoid the execution of the default file 
    elif args.from_file:
        the_file = pathlib.Path(args.from_file)
        core_execution(manage_file.txt_to_list(the_file), sha_protocol)
        manage_file.keep_passwords_safe(the_file)
        sys.exit() 

if __name__ == '__main__':
    main()
    
    

        