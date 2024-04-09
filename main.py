# -*- coding: utf-8 -*-
import API_functions 
import sys

# ESECUZIONE DEL PROGRAMMA
# TODO introduce a cl to get the password from a block note path, then
def main(argomenti):
    for password in argomenti:
        count = API_functions.conta_trapelate(API_functions.pwned_API_check(password))
        if count:
            print(f'{password} è stata hackerata {count} volte')
        # TODO introduce a suggestion to create a password
        else:
            print(f'{password} è sicura')
    return 'finito'
# TODO blank the note and then overwrite in the same location to remove definitely the password existence from the local
if __name__ == '__main__' :
    sys.exit(main(sys.argv[1:]))
    
    