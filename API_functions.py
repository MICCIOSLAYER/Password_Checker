import requests
import hashlib



def richiedi_dati_API(query) -> requests.Response : # insert the pass to check to get a response
    '''
    get the response from the API, if the status code is not 200, raise an error

    Parameters
     query : any - the password to check ( better if in hexdigest format)    
     response : requests.Response - the response from the API
    '''
    query_str = str(query)
    url = 'https://api.pwnedpasswords.com/range/' + query_str
    response = requests.get(url)
    if response.status_code != 200: 
        raise RuntimeError(f'errore Fetching?? {response.status_code}, controlla l\'api e prova ancora')
    return response


def conta_trapelate(tupla : tuple) -> int: 
    '''
    split the hashes to get the count of violation ( after :), 
    if the 2nd param matches the count of violation,
    the function returns this value, otherwise 0
    this let us know the number of violations without inserting the full password, in hexdigest format
    
    Parameters
    tupla : tuple - the tuple that contains the response from the API and the password to check
    count : int - the count of violation of the password registered

    '''
    hashes = tupla[0]
    hash_to_check = tupla[1]

    hashes = (line.split(':') for line in hashes.text.splitlines()) # get the count of violation from hashes
    for h, count in hashes:
        if h == hash_to_check.upper(): # sometimes happens that the hash_to_check is in lower case
            return int(count)
    return 0 # as default return 0 if the password is not in the list ( dictionary)


def pwned_API_check(password : str, sha256=False) -> tuple: # sha256 is a flag to use the sha256 protocol
    '''
    check if the password exists in the API, then get the API response and the rest of conversion
    
    Parameters
    password : str - the password to convert 
    sha256 : bool - the flag to use the sha256 protocol or not
    tuple([risposta, restanti]) : tuple - the tuple that contains the response from the API and the rest of the conversion

    '''    
    sha1Pass = hashlib.sha1(password.encode('utf-8')).hexdigest()  # convert through sha1 for privacy reasons
    primi5, restanti = sha1Pass[:5], sha1Pass[5:]  # separa i primi 5 caratteri della conversione dal resto
    risposta = richiedi_dati_API(primi5)  # immagazzina i primi 5 caratteri della conversione nella risposta
    
    if(sha256==True): # in case the protocol request is sha256
        sha256Pass = hashlib.sha256(password.encode('utf-8')).hexdigest()  
        primi5, restanti = sha256Pass[:5], sha256Pass[5:]
        risposta = richiedi_dati_API(primi5)
        return tuple([risposta, restanti])
       
    return tuple([risposta, restanti])  # need a tuple cause the order is important 
