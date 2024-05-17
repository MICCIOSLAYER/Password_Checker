import argparse
from Password_Checker.modules import manage_file 
from Password_Checker.modules import API_functions 
from Password_Checker.modules import Textuals 
import pathlib
import os
from pathlib import Path
import getpass
import logging

logging.basicConfig(level=logging.DEBUG, filename='log.log',filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# ESECUZIONE DEL PROGRAMMA 2.0
def core_execution(passwords_list : list, sha_protocol : bool)-> None: # a function to slim the code in main()
    '''
    Parameters:
    - passwords_list : list - the list of passwords to check
    - sha_protocol : bool - the protocol to use
    '''
    # 
    if len(passwords_list) <= 0:
        print('the list is empty, no passwords to check')
    else:
        for password in passwords_list:
            count = API_functions.conta_trapelate(API_functions.pwned_API_check(password, sha256=sha_protocol))
            if count:
                print(f'\'{password}\' has been hacked {count} times')
            else:
                print(f'\'{password}\' is not been hacked')
    return None




def main():
    logging.basicConfig(filename='myapp.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%D %H:%M:%S')

    desktop_path = pathlib.Path(os.path.expanduser("~/Desktop")) # put them in a config files?
    txt_file_default = desktop_path / 'default_list.txt'
    
    parser = argparse.ArgumentParser(description='check the security of your passwords')
    sha256_protocol = parser.add_argument('--sha256', help='use the sha256 protocol', action='store_true')

    reading_mode = parser.add_mutually_exclusive_group(required=True) 
    parser_pwcl = reading_mode.add_argument('-l' , 'from_here', help='input the passwords here', action='store_true') 
    parser_file = reading_mode.add_argument('-f' , 'from_file', type=Path, help='input the path to password\'s file, otherwise remember to fill the default file in your Desktop', default=manage_file.default_file_path()) 
    parser_example = reading_mode.add_argument('-ex', 'example', help='use an example to show the program', action='store_true')
    
    verification_parser = parser.add_argument('-v', '--verify', help='verify the code behaviour', type=Path)

    args =  parser.parse_args()
    sha_protocol = args.sha256
    if sha_protocol: 
        logging.warn('this option is not available yet, then the passwords will be checked with sha1 protocol')
        sha_protocol = False  #since not implemented yet

    if args.from_here: 
        passwords_list = getpass.getpass(prompt='insert the passwords here, separated by space (then ENTER): ').split()
        core_execution(passwords_list, sha_protocol)

    elif args.from_file:
        the_file = pathlib.Path(args.from_file)
        core_execution(manage_file.txt_to_list(the_file), sha_protocol)
        manage_file.keep_passwords_safe(the_file)
        

    elif args.example:
        example_path = manage_file.example_file() #HACK after testing replace the path with a simple list of strings
        core_execution(manage_file.txt_to_list(example_path), sha_protocol)
        print('since this is an example, the passwords are casual and to be cancelled by the real file once the code is ok')

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
    
    

        