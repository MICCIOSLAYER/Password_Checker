import os
"""options = { 
    '-f' : reading_mode.read_from_file(argomenti[1]), 
    '-l' : reading_mode.read_from_list(argomenti[1:]) 
    }
if argomenti[0] in options:
    passwords_list = options[argomenti[0]]""" # nel caso di voler usare un dizionario per le opzioni

def read_from_file(path : str) -> list: # if is_path is True, the path is a file, otherwise is a list
    print('reading from file...')
    
    with open(path, 'r') as f: # TODO check if f is not empty

        pw_list = f.readlines()
        passwords_list = [pw.strip() for pw in pw_list]
    return passwords_list


def read_from_list(passwords : list) -> list:
    passwords_list = passwords[:]
    return passwords_list