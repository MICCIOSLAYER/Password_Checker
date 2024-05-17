#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import pathlib
from pathlib import Path
import os
import logging
import sys


def txt_to_list(txt_file : pathlib.Path ) -> list[str]: # FIXED
    '''
    get the list of passwords from the note
    
    Parameters:
    path : str - the absolute-path of the note from which to get the passwords
    '''
     
    try:
        if str(txt_file)[-4:]  != '.txt': 
            logging.critical(f'{txt_file} is not a txt file')
            raise TypeError('this is not a txt file')
        with open(txt_file, 'r', encoding='utf-8', errors='strict') as f: # to avoid unreadable character use a default encoding depending on your pc? or better to use utf-8
                passwords_list = f.read().split()
                f.close()
                if len(passwords_list) == 0:
                    logging.warning('no passwords are stored here')
    except TypeError: 
        return 'this is not a txt file'
    except FileNotFoundError: 
        logging.critical(f'file {txt_file} not found')
        return 'file not found'
    except ValueError as e: # if a decoding error occurs open(error=strict by default) raise a ValueError
        logging.critical(f'{e} use a UTF-8 encoded file to store your passwords')
        return 'Unreadable file, assure to use a UTF-8 encoded file to store your passwords'

    except Exception as e: # HOWTO test this? 
        logging.debug(f'{e} during the reading of the file {txt_file}')
        return 'Unexpected exception read the log file for more details'
    
    else:            
            return passwords_list
    
     
            
def default_file_path() -> pathlib.Path: # FIXED 
    '''                                                 con path  = txt_file_default (oggetto pathlib.Path)
    creation/ read of a file to read passwords by a default path in Desktop
    '''
    
    desktop_path = pathlib.Path(os.path.expanduser("~/Desktop"))
    txt_file_default = desktop_path / 'default_list.txt' # TODO replace it with a config file object
    content = 'D_default_path4 these@password isins1de thi5Pc'  # TODO replace it with a config file object
    logging.info(f'this is a default_path list of passwords: {txt_file_default}')

    
    if os.path.exists(txt_file_default):  # if exists write it if blank
        with open(txt_file_default, 'r+', encoding='utf-8') as b: 
            if b.read() == '':  # to avoid the overwrite of the file if not empty
                logging.warning(f'the file {txt_file_default} is blank, then it will be overwritten')
                b.write(content) 
            b.close()

    else:   # if not exists create it
        txt_file_default.parent.mkdir(exist_ok=True, parents=True)
        with open(txt_file_default, 'w', encoding='utf-8') as f:
            logging.info(f'since {txt_file_default} is not found, it will be created')
            f.write(content)  # TODO replace it with a config file object
            f.close()

    return (txt_file_default)

    

def keep_passwords_safe(txt_file : pathlib.Path) -> None:
    '''
    overwrite the file with a blanck note to keep safe your passrords

    Parameters:
    txt_file : Path - the absolute-path of the note containing your passwords to overwrite
    '''
    
    try:
        if os.path.exists(txt_file):        
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.seek(0)
                f.write('')
                f.close()
        else:
            raise FileNotFoundError
        
    except FileNotFoundError as e:
        logging.critical(f'{e} : file {txt_file} not found, something went wrong in meantime')
        return 'Something went wrong while overwriting the file, where stored the passwords'
    else: 
        logging.info('the note is now blank, your passwords are safe')
        return 'Passwords aren\'t leaked'

def example_file() -> pathlib.Path:
    '''
    creation/ read of a file to read passwords by a default path in Desktop
    '''
    example_path = pathlib.Path.home() / 'Check_these_passwords' / 'example_list.txt'  # TODO replace it with a config file object
    content = 'today@is @b34UtIfull \nTh4n Y3sterd@y'   # TODO replace it with a config file object
    example_path.parent.mkdir(exist_ok=True, parents=True)
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()
        return example_path
