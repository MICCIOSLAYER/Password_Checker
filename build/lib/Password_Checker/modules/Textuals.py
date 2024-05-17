#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

def Description() -> str: # FIXME put this description in the readme file

    print('''this is a program to check the security of your passwords: \n
          please compose the command as follows: python3 main.py <PROTOCOL> <PATH>, where: \n
          - <PROTOCOL> is the protocol to use (sha1 or sha256) \n
          - <PATH> is the path to the file containing the passwords to check \n
          - if you want to check a list of passwords, please insert them as arguments in place of <PATH>,
            however this option is strongly discouraged since you lose all your control
            in where the password name is saved in current local disk \n''')
    return ''

def Suggestion_for_a_password (count_of_violation : int) -> str:
    '''
    Parameters:
    count_of_violation : int - depending from this number, the function gives a suggestion for a new password
    '''
    if count_of_violation > 100 :
        print('''a suggestion for a new password: \n
              use a Capital letter, a number, a special character and a length of at least 8 characters \n
              ''')
    return ''