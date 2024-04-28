import argparse
import manage_file
import API_functions
import Textuals
import pathlib
import os
from pathlib import Path
import getpass

# ESECUZIONE DEL PROGRAMMA 2.0
def main_execution(passwords_list : list, sha_protocol : bool)-> None: # a function to slim the code in main()
    '''
    Parameters:
    passwords_list : list - the list of passwords to check
    sha_protocol : bool - the protocol to use
    '''
    assert len(passwords_list) > 0, 'the list is empty, no passwords to check'

    for password in passwords_list:
        count = API_functions.conta_trapelate(API_functions.pwned_API_check(password, sha256=sha_protocol))
        if count:
            print(f'\'{password}\' has been hacked {count} times')
        else:
            print(f'\'{password}\' is not been hacked')
    return None




def main():
    # as default <name> <protocol as default sha1> <read_mode as default from a specified test> <passswlist or path> -> 
    # if read mode is -l list getpass.getpass()
    # if read mode is -f read from file put a default path to check, otherwise if specified add a path
    parser = argparse.ArgumentParser(description='check the security of your passwords')

    #protocol_type = parser.add_parsers(help='select the protocol to use', dest='protocol')

    # to be used as default sha1_protocol = parser.add_parser('-sha1', help='use the sha1 protocol', action='store_true')

    sha256_protocol = parser.add_argument('--sha256', help='use the sha256 protocol', action='store_true')

    #reading_mode = parser.add_mutually_exclusive_group() #is it necessary?
    parser_pwcl = parser.add_argument('-l' , '--listed', help='input the passwords here', action='store_true') #reading_mode?
    parser_file = parser.add_argument('-f' , '--from_file', type=Path, help='input the path to password\'s file, remember to put a password per line in the file') #reading_mode?
    default_execution = parser.add_argument('-d', '--default_path', help='use the default path to check the passwords', action='store_true')
    # FIXME  add an example parser and use a default executionto run the program, create a new default txt

    verification_parser = parser.add_argument('-v', '--verify', help='verify the code behaviour', type=Path)

    args =  parser.parse_args()
    sha_protocol = args.sha256
    if sha_protocol: #since not tested yet
        print('this option is not available yet, then the passwords will be checked with sha1 protocol')
        sha_protocol = False

    if args.listed: 
        passwords_list = getpass.getpass(prompt='insert the passwords here, separated by space (then ENTER): ').split()
        main_execution(passwords_list, sha_protocol)

    if args.from_file:
        file_path = pathlib.Path(args.from_file) 
        passwords_list = manage_file.txt_to_list(file_path)
        main_execution(passwords_list, sha_protocol)
        manage_file.keep_passwords_safe(file_path)
        assert manage_file.note_is_empty(file_path), 'the passwords are not safe'

    if args.default_path:
        default_path = manage_file.default_file_path()
        passwords_list = manage_file.txt_to_list(default_path)
        assert passwords_list, 'the list is empty, no passwords to check' # HACK something similar
        main_execution(passwords_list, sha_protocol)
        manage_file.keep_passwords_safe(default_path)
        assert manage_file.note_is_empty(default_path), 'the passwords are not safe'

    if args.verify: # continua a testare, -> testa il default path execution  per scrivere un contenuto aggiuntivo 
        verification = type(args.verify)

        print(f'{type(pathlib.Path(os.path.expanduser("~/Desktop")))} è il tipo di dato di {pathlib.Path(os.path.expanduser("~/Desktop"))}')
        desktop_path = pathlib.Path(os.path.expanduser("~/Desktop"))
        txt_file = desktop_path / 'default_list.txt'
        with open(txt_file, 'r', encoding='utf-8') as f:
            testo = f.read()
            f.close()
        print(f'{testo} è il contenuto del file {txt_file}')
if __name__ == '__main__':
    main()
    
    

        