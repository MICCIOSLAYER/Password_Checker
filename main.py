# -*- coding: utf-8 -*-
import API_functions 
import Reading_mode
import API_functions
import os
import sys
import path_for_safe
# ESECUZIONE DEL PROGRAMMA

def main(list_of_interest : list) -> str: # from a list of object get the password to check and the protocol to use
    Reading_mode.Description() 

    while(len(list_of_interest) < 2): # to avoid indexing errors
        print('please insert the protocol and the <PATH> containing the passwords to check:')
        list_of_interest = input().split(' ')
    
    file_path = False   # initialize to use as a flag
    sha256 = (str(list_of_interest[0]).lower() == 'sha256') #to use the selection of sha256 or sha1 in pwned_API_check

    if os.path.exists(list_of_interest[1]): #in case the second term is a file:
        try: # control if it is empty
            if path_for_safe.note_is_empty(list_of_interest[1]):
                sys.exit('please insert some passwords to check in the file')
            file_path = list_of_interest[1] 
            passwords_list = Reading_mode.read_from_file(file_path)
        except FileNotFoundError:    # to not crush in case file is not found
            sys.exit(f'file {list_of_interest[1]} not found')

    else :
        passwords_list = list_of_interest  # if not a path assume there's a list of passwords

    for password in passwords_list:

        count = API_functions.conta_trapelate(API_functions.pwned_API_check(password, sha256))
        max_count = 0

        if count:
            max_count = max(max_count, count) # NOTE it is better to use a sum than a product?
            print(f'\'{password}\' has been hacked {count} times')
            
        else:
            print(f'{password} is safe')

    Reading_mode.Suggestion_for_a_password(max_count)

    if file_path:   # overwrite the file with a blanck note to keep safe your passrords
        path_for_safe.overwrite_blanck_note(file_path)  
    
    return 'something else to check?'

if __name__ == '__main__' :
    
    sys.exit(main(sys.argv[1:]))
    
    