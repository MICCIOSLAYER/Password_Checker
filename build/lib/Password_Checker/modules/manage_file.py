#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'


from pathlib import Path
import os
import logging

def txt_to_list(txt_file : Path ) -> list[str]: 
    '''
    Put the txt file content in a list of Strings
    
    Parameters:
    path : str - the absolute-path of the note from which to get the passwords
    '''
    try:
        if str(txt_file)[-4:]  != '.txt': 
            logging.critical(f'{txt_file} is not a txt file') 
            raise TypeError('this is not a txt file')
       
        with open(txt_file, 'r', encoding='utf-8', errors='strict') as f: 
                passwords_list = f.read().split()
                f.close()
                if len(passwords_list) == 0:
                    logging.warning('no passwords are stored here')

    except FileNotFoundError: 
        logging.exception(f'file {txt_file} not found') 
        return 'file not found'
    except ValueError as e: #for completeness eve if the test doesn't seems to care
        logging.exception(f'{e} use a UTF-8 encoded file to store your passwords')
        return 'Unreadable file, assure to use a UTF-8 encoded file to store your passwords'
    except Exception as e: 
        logging.exception(f'{e} during the reading of the file {txt_file}')   
        return 'Unexpected exception read the log file for more details'
    
    else:            
            return passwords_list
    
     
            
def default_file_path() -> Path:
    '''                                                 
    creation/ read of a file to read passwords by a default path in Desktop
    if nothing inside put some content as a default content
    '''
    
    desktop_path = Path(os.path.expanduser("~/Desktop"))
    txt_file_default = desktop_path / "default_list.txt"
    content = 'D_default_path4 these@password isins1de thi5Pc'
    logging.debug(f'this is a default_path list of passwords: {txt_file_default}')

    
    if os.path.exists(txt_file_default):  
        with open(txt_file_default, 'r+', encoding='utf-8') as b: 
            blanked= b.read() ==  ''
            if blanked:  #  overwrite of the file if empty
                b.write(content) 
            b.close()
        if blanked: # necessary outside to logging correctly
            logging.warning(f'the file {txt_file_default} is blank, then it will be overwritten')

    else:   # if not found in designated path create it
        logging.warning(f'since {txt_file_default} is not found, it will be created')
        txt_file_default.parent.mkdir(exist_ok=True, parents=True)
        with open(txt_file_default, 'w', encoding='utf-8') as f:  
            f.write(content)  
            f.close()

    return (txt_file_default)

    

def keep_passwords_safe(txt_file : Path) -> None:
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
        logging.exception(f'{e} : file {txt_file} not found, something went wrong in meantime')  
        return 'Something went wrong while overwriting the file, where stored the passwords'
    else: 
        logging.info('the note is now blank')  
        return 'Passwords aren\'t leaked'

def example_file() -> Path:
    '''
    creation of a file as an example 
    '''
    example_path = Path.home() / "Check_these_passwords" / "example_list.txt"
    content = 'today@is @b34UtIfull\nTh4n Y3sterd@y'
    example_path.parent.mkdir(exist_ok=True, parents=True)
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(content)
        f.close()
        return example_path
