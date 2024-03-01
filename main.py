# -*- coding: utf-8 -*-
import requests
import hashlib
import sys

# definisce LA CLASSE RISPOSTA a una richiesta effettuata su un http
def richiedi_dati_API(query):
    '''
verifica la sicurezza di una password

    '''
    query_str = str(query)
    url = 'https://api.pwnedpasswords.com/range/' + query_str
    risposta = requests.get(url)
    if risposta.status_code != 200:
        raise RuntimeError(f'errore Fetching?? {risposta.status_code}, controlla l\'api e prova ancora')
    return risposta

# dall'algoritmo di hashing separa i conteggi dall'hash sha1 della password e ne confronta i risultati con la lista di quelli forniti dal sito
def conta_trapelate(hashes, hash_da_controllare):
    '''
    dato il foramto delle hashes separiamole in liste da 2 elementi ciasdcuna,
    di cui il secondo è tutto ciò che si trova dopo i :
    avendo separato i dati, se il secondo parametro corrisponde al conteggio delle violazioni,
    viene restituito tale valore
    in questo modo senza dover inserire la password completa, nel formato hexdigest,
    viene estrapolato il numerp di violazioni

    '''
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_da_controllare.upper():

            return count
    return 0
    
#  restituisce il conteggio di violazioni della password quando i primi 5 caratteri dell'hash della password corrispondono a
def pwned_API_check(password):
    '''
    check se la password esiste nella risposta dell'API

    '''
    sha1Pass = hashlib.sha1(password.encode('utf-8')).hexdigest()  # converte la password in sha1
    primi5, restanti = sha1Pass[:5], sha1Pass[5:]  # separa i primi 5 caratteri della conversione dal resto
    risposta = richiedi_dati_API(primi5)  # immagazzina i primi 5 caratteri della conversione nella risposta
    return conta_trapelate(risposta, restanti) # restituisce un risultato != 0 se il testo della risposta corrisponde ai restanti

# ESECUZIONE DEL PROGRAMMA
def main(argomenti):
    for password in argomenti:
        count = pwned_API_check(password)
        if count:
            print(f'{password} è stata hackerata {count} volte')
        else:
            print(f'{password} è sicura')
    return 'finito'

if __name__ == '__main__' :
    sys.exit(main(sys.argv[1:]))
    
    