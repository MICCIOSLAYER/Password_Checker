import os
"""options = { 
    '-f' : reading_mode.read_from_file(argomenti[1]), 
    '-l' : reading_mode.read_from_list(argomenti[1:]) 
    }
if argomenti[0] in options:
    passwords_list = options[argomenti[0]]""" # FIXME this is a snippet of code to use in main.py when the options are fixed

def read_from_file(path : str) -> list: # if is_path is True, the path is a file, otherwise is a list
    '''
    Parameters:

    path : str - the path to the file to read

    '''
    print('reading from file...')
    
    with open(path, 'r') as f: 

        pw_list = f.readlines()
        passwords_list = [pw.strip() for pw in pw_list]
    return passwords_list


def read_from_list(passwords : list) -> list:
    '''
    Parameters:
    passwords : list - the list of passwords to put in a list
    '''
    passwords_list = passwords[:]
    return passwords_list

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