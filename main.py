# -*- coding: utf-8 -*-
import API_functions 
import Reading_mode
import API_functions
import os
import sys
import path_for_safe
# ESECUZIONE DEL PROGRAMMA

def main(argomenti):
    file_path = False   # initialize to use as a flag
    
    if os.path.exists(argomenti[0]): #in case the first term is a file:
        try: # control if it is empty
            if path_for_safe.note_is_empty(argomenti[0]):
                sys.exit('please insert some passwords to check in the file')
            file_path = argomenti[0] 
            passwords_list = Reading_mode.read_from_file(file_path)
        except FileNotFoundError:    # to not crush in case file is not found
            sys.exit(f'file {argomenti[0]} not found')

    else :
        passwords_list = argomenti  # if not a path assume there's a list of passwords

    for password in passwords_list:
        count = API_functions.conta_trapelate(API_functions.pwned_API_check(password))
        if count:
            print(f'\'{password}\' has been hacked {count} times')
        # TODO introduce a suggestion to create a password
        else:
            print(f'{password} is safe')
    
    if file_path:   # overwrite the file with a blanck note to keep safe your passrords
        path_for_safe.overwrite_blanck_note(file_path)  
    
    return 'something else to check?'

if __name__ == '__main__' :
    sys.exit(main(sys.argv[1:]))
    
    