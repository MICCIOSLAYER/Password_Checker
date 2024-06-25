#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import requests
import hashlib
import logging
from requests.exceptions import HTTPError
from pathlib import Path


def API_response(query: any) -> requests.Response:
    '''

    Get the response from the API, if the status code is not ok, log an error

    Parameters:
    --------
    query : any - the password to check ( better if in hexdigest format) 

    Returns:
    --------   
    response : Response - the response from the API 

    '''
    try:
        query_str = str(query)
        url = 'https://api.pwnedpasswords.com/range/' + query_str
        response = requests.get(url, timeout=5)
        response.raise_for_status()

    except HTTPError:
        print(f'''HTTPError: the query {query} has raised an error {response.status_code}: 
              for more information check the log file or visit the website:
              https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages''')
        if response.status_code in [400, 401, 403, 404]:
            logging.error(
                f'Client error: verify your connection & account and retry later')
            return 'Client error'
        elif response.status_code == 429:
            logging.error(
                f'Client error: Too many requests, please split the file/list and retry')
            return 'Client error'
        elif response.status_code == 503:
            logging.error(
                f'Server error: Service Unavaiable, please retry later')
            return 'Server error'
    else:
        if response.ok:  # between 200 and 299
            return response


def leaked_count(tupla: tuple) -> int:
    '''
    Split the hashes to get the count of violation ( after :).

    Parameters:
    ----------
    tupla : tuple - the tuple whose info are:
        tuple[0] - the response from the API representing the list of sha1_converted-hacked-words with the same firsts five characters,
                   omitted by the output
        tuple[1] -  the password conversion in sha1 protocol [5:] characters to search the match in the list of hashes (tupla[0])

    Returns:
    ---------
    count : int - the count of violation of the password registered

    '''

    hashes = tupla[0]
    hash_to_check = tupla[1]

    # get the count of violation from hashes
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0  # not found = not violated


def pwned_API_check(password: str, sha256=False) -> tuple:
    '''
    Prepare the input format for the API, and store both the input and output, in respective format, for final check 

    Parameters:
    ----------
    password : str - the password to check and format  
    sha256 : bool - the flag to use the sha256 protocol or not NOTE NOT YET AVAIABLE

    Returns:
    --------
    tuple([answer, match_by_list]) : tuple - the output from which extract the count of violations
        - answer : The API Response
        - match_by_list : the remaining part of the password_conversion to check in the list of hashes
    '''
    sha1Pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    to_put_into_api, match_by_list = sha1Pass[:5], sha1Pass[5:]
    # since the url request the first 5 @@@@@ of conversion to get the list of hashes violated
    answer = API_response(to_put_into_api)

    if sha256 == True:
        sha256pass = hashlib.sha256(
            password.encode('utf-8').hexdigest()).upper()
        to_put_into_api, match_by_list = sha256pass[:5], sha256pass[5:]
        answer = API_response(to_put_into_api)  # TODO  avoid in-call

    return tuple([answer, match_by_list])
