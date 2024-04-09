# -*- coding: utf-8 -*-
import API_functions 
import Reading_mode
import API_functions
import os
import sys
import path_for_safe
# ESECUZIONE DEL PROGRAMMA

def main(argomenti):
    
    if os.path.exists(argomenti[0]): #in case the first term is a file:
        try:
            if path_for_safe.note_is_empty(argomenti[0]):
                sys.exit('please insert some passwords to check in the file')
            file_path = argomenti[0] 
            passwords_list = Reading_mode.read_from_file(file_path)
        except FileNotFoundError:    
            sys.exit(f'file {argomenti[0]} not found')

    else :
        passwords_list = argomenti

    for password in passwords_list:
        count = API_functions.conta_trapelate(API_functions.pwned_API_check(password))
        if count:
            print(f'\'{password}\' has been hacked {count} times')
        # TODO introduce a suggestion to create a password
        else:
            print(f'{password} is safe')
    
    if file_path:
        path_for_safe.overwrite_blanck_note(file_path)
    
    return 'please re:type to run again the code'
# TODO blank the note and then overwrite in the same location to remove definitely the password existence from the local
if __name__ == '__main__' :
    sys.exit(main(sys.argv[1:]))
    
    