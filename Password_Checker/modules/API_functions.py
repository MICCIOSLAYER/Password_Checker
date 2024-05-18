#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import requests
import hashlib
import logging
from requests.exceptions import HTTPError

#CONFIGURATION OF LOGGING



def richiedi_dati_API(query : any) -> requests.Response : # TODO change the name  in get_response_from_API
    '''
    get the response from the API, if the status code is not 200, raise an error

    Parameters
     query : any - the password to check ( better if in hexdigest format)    
     response : requests.Response - the response from the API
    '''
    try:
        query_str = str(query) # HACK?  CONVERT HERE to avoid the pwned API
        url = 'https://api.pwnedpasswords.com/range/' + query_str
        response = requests.get(url, timeout=5)
        #response.raise_for_status() # raise an error if the status code is not 200 HACK x test use a mock response HOWTO?
        
    except HTTPError:
        logging.exception(f'HTTPError: the query {query} has raised an error {response.status_code}') 
        if response.status_code in [400, 401, 403, 404]:
            logging.error(f'Client error: verify your connection & account and retry later')
            return 'Client error'
        elif response.status_code == 429:
            logging.error(f'Client error: Too many requests, please split the file/list and retry')
            return 'Client error'
        elif response.status_code == 503:
            logging.error(f'Server error: Service Unavaiable, please retry later')
            return 'Server error'
        elif (response.status_code in range(100, 200) or response.status_code in range(300, 601)):
            logging.error(f'For more information check the logs and visit the website: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages')
            return 'Unexpected Error'
    else:
        if response.ok: # between 200 and 299 
            return response
    finally:
        if  not response.ok:
            logging.error(f'HTTPError: the query {query} has raised an error {response.status_code}') 
    


def conta_trapelate(tupla : tuple) -> int: 
    '''
    split the hashes to get the count of violation ( after :), 
    if the 2nd param matches the count of violation,
    the function returns this value, otherwise 0
    this let us know the number of violations without inserting the full password, in hexdigest format
    
    Parameters
    tupla : tuple - the tuple that contains:
        tuple[0] the response from the API as a list of hashes-words-converted with the same first 5 characters in sha1 protocol
        tuple[1] the password conversion [5:] to search in the list of hashes
    count : int - the count of violation of the password registered

    '''
    # body of try:
    hashes = tupla[0] 
    hash_to_check = tupla[1]
    
    hashes = (line.split(':') for line in hashes.text.splitlines()) # get the count of violation from hashes
    for h, count in hashes:
        if h == hash_to_check: 
            return int(count)
    return 0 # not found = not violated

def pwned_API_check( password : str, sha256=False ) -> tuple: #  HACK control the rest of code considering the added parameter server_response : requests.Response,..
    '''
    check if the password exists in the API, then get the API response and the rest of conversion
    
    Parameters
    password : str - the password to convert 
    sha256 : bool - the flag to use the sha256 protocol or not
    
    tuple([answer, remaining]) : tuple - the tuple that contains the query to put into the API_web_site and the rest of the conversion to extract (through a match) the exact count of violations
    the tuple division is necessary since the website API works in this way
    '''    
    sha1Pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()  
    to_put_into_api, match_by_list = sha1Pass[:5], sha1Pass[5:]  
    answer = richiedi_dati_API(to_put_into_api)  # since the url request the first 5 @@@@@ of conversion to get the list of hashes violated HACK set answer = server_response
    
    if sha256 == True: 
        sha256pass = hashlib.sha256(password.encode('utf-8').hexdigest()).upper()                
        to_put_into_api, match_by_list = sha256pass[:5], sha256pass[5:]
        answer = richiedi_dati_API(to_put_into_api) # HACK in future rewrite to avoid in-call
       
    return tuple([answer, match_by_list])  
