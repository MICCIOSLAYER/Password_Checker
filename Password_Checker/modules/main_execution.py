from modules import API_functions
import sys

# PROGRAM EXECUTION


def core_execution(
        passwords_list: list,
        verbosity: bool
) -> None:  # a function to slim the code in main()
    '''
    Represent the core execution of the code pourpose it get counts of leaks from a list of passwords

    Parameters:
    - passwords_list : list - the list of passwords to check
    - sha_protocol : bool - the protocol to use

    Returns:
    None, However it prints a different string depending on the leaks of your passwords
    - if the input doesn't match the requirements the core exit and prints a message 
    '''

    if type(passwords_list) != list:
        print(
            'TypeError : the input is not a list, for more information check the log file')
        sys.exit()

    if len(passwords_list) <= 0:
        print('the list is empty, no passwords to check')
        sys.exit()

    else:
        sha_protocol = False  # when implemented & add a parameter to function
        count_records = []
        for password in passwords_list:
            count = API_functions.leaked_count(
                API_functions.pwned_API_check(password, sha256=sha_protocol))
            count_records.append(count)
            if count:
                print(f'\'{password}\' has been hacked {count} times')
            else:
                print(f'\'{password}\' is not been hacked')
        if (max(count_records) and verbosity):
            print('''For a better choise of your passwords, you can add some number and special caracters,
remember to always include both capital letter and lower letter, with at least of 8 characters.
                  ''')
    return None
