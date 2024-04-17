import argparse
import path_for_safe
import API_functions


# ESECUZIONE DEL PROGRAMMA 2.0
# as default <name> <protocol> <read_mode> <passswlist or path> -> 
# if read mode is -l list getpass.getpass()
# if read mode is -f read from file put a default path to check, otherwise if specified add a path
parser = argparse.ArgumentParser(description='check the security of your passwords')

protocol_type = parser.add_subparsers(help='select the protocol to use', dest='protocol')

sha1_protocol = protocol_type.add_parser('sha1', help='use the sha1 protocol')

sha256_protocol = protocol_type.add_parser('sha256', help='use the sha256 protocol', action='store_true')

from_interface = parser.add_subparsers('-l' or 'list', help='input the passwords here', dest='read_mode')

from_file = parser.add_subparsers('-f' or 'file', help='input the path to password\'s file', dest='read_mode')