# -*- coding: utf-8 -*-
import functions 
import sys

# ESECUZIONE DEL PROGRAMMA
def main(argomenti):
    for password in argomenti:
        count = functions.conta_trapelate(functions.pwned_API_check(password))
        if count:
            print(f'{password} è stata hackerata {count} volte')
        else:
            print(f'{password} è sicura')
    return 'finito'

if __name__ == '__main__' :
    sys.exit(main(sys.argv[1:]))
    
    