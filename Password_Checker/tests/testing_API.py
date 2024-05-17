#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
import random
import responses
import hashlib
from Password_Checker.modules.API_functions import richiedi_dati_API, conta_trapelate, pwned_API_check
import logging

# testing the API_functions module
class Test_API_Module_right_work(unittest.TestCase):
  
    # TEST richiedi_dati_API-----------------------------------------------------
    @responses.activate
    def test_richiedi_dati_API_status_code(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'hello' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646', # a part of the response.text 
            status=200
        )
        response = richiedi_dati_API(converted_pass[:5])
        self.assertEqual(response.status_code, 200)
        
    
    @responses.activate
    def test_richiedi_dati_API_response_content(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'hello' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646', # a part of the response.text 
            status=200
        )
        response = richiedi_dati_API(converted_pass[:5])
        self.assertEqual(response.text, '000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646')


    # TEST conta_trapelate-----------------------------------------------------
    @responses.activate
    def test_leaked_count_higher_than_0(self):
        # compulsory to get the response type from the API
        query = 'hello' 
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646', # a part of the response.text 
            status=200
        )
        hashes = richiedi_dati_API(converted_pass[:5])

        hash_to_check = '61DDCC5E8A2DABEDE0F3B482CD9AEA9434D'
        tupla = (hashes, hash_to_check)
        leaks = conta_trapelate(tupla)
        self.assertEqual(leaks, 273646)

    @responses.activate
    def test_leaked_ZEROcount(self):
        # compulsory to get the response type from the API
        query = 'hello' 
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646', # a part of the response.text 
            status=200
        )
        hashes = richiedi_dati_API(converted_pass[:5])

        hash_to_check = '61DDCE5E8A2DABEDE0F3B482CD9AEA9434D' # invented hash
        tupla = (hashes, hash_to_check)
        leaks = conta_trapelate(tupla)
        self.assertEqual(leaks, 0)

    @responses.activate
    def test_pwned_API_check_the_search_key(self):
        # compulsory to get the response type from the API
        query = 'hello' 
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646', # a part of the response.text 
            status=200
        )
        resulted_tuple = pwned_API_check(query)
        expected_tuple = (richiedi_dati_API(converted_pass[:5]), '61DDCC5E8A2DABEDE0F3B482CD9AEA9434D')
        self.assertEqual(resulted_tuple[1], expected_tuple[1])
    
    @responses.activate
    def test_pwned_API_check_the_server_response(self):
        # compulsory to get the response type from the API
        query = 'hello' 
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646', # a part of the response.text 
            status=200
        )
        resulted_tuple = pwned_API_check(query)
        expected_tuple = (richiedi_dati_API(converted_pass[:5]), '61DDCC5E8A2DABEDE0F3B482CD9AEA9434D')
        self.assertEqual(resulted_tuple[0].content, expected_tuple[0].content)

class Test_API_Module_fails(unittest.TestCase):
    @responses.activate
    def test_richiedi_dati_API_error_4xx(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'random' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        error_4xx = [400, 401, 403, 404]
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=random.choice(error_4xx)
        )
        response = richiedi_dati_API(converted_pass[:5])
        self.assertEqual(response, 'Client error, verify your connection & account and retry later')

    @responses.activate
    def test_richiedi_dati_API_error_429(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'random' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=429
        )
        response = richiedi_dati_API(converted_pass[:5])
        self.assertEqual(response, 'Client error: Too many requests, please split the file/list and retry')

    @responses.activate
    def test_richiedi_dati_API_error_503(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'random' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=503
        )
        response = richiedi_dati_API(converted_pass[:5])
        self.assertEqual(response, 'Server error: Service Unavaiable, please retry later')

    @responses.activate
    def test_richiedi_dati_API_error_random_error(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'hello' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=303
        )
        response = richiedi_dati_API(converted_pass[:5])
        self.assertEqual(response.status_code, 303)

class Test_API_Module_logs(unittest.TestCase):
    #TEST LOGS****************************************************************
    @responses.activate
    def test_richiedi_dati_API_response_content(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'hello' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            status=400)
        print(richiedi_dati_API(converted_pass[:5]))
        '''with self.assertLogs(logger=logging.getLogger(__name__), level=logging.DEBUG) as cm:
            richiedi_dati_API(converted_pass[:5])
        print(cm.output[0])
        self.assertIn('HTTPError', cm.output[0])'''
        
class Test_API_Module_combined(unittest.TestCase):
    # use a multiple called from a multiple responses
    #use the query as distinctive element, as for query in list : base_url + query, then get response from leaked_count(query) and check
    # see: https://pypi.org/project/responses/#matching-requests
    @responses.activate
    def test_final_combination_API_functions_module(self):

        query1 = 'hello'
        converted_pass1 = hashlib.sha1(query1.encode('utf-8')).hexdigest().upper()
        query2 = 'world'
        converted_pass2 = hashlib.sha1(query2.encode('utf-8')).hexdigest().upper() # TODO get a body part of this response w world conv
        query3 = 'random'
        converted_pass3 = hashlib.sha1(query3.encode('utf-8')).hexdigest().upper() # TODO get a body part of this response w/o random conv
        list_of_queries = [converted_pass1[:5], converted_pass2[:5], converted_pass3[:5]]
        pass_list = [query1, query2, query3]

        responses.get(
            url = 'https://api.pwnedpasswords.com/range/' + converted_pass1[:5],
            body= '000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',
            status=200
        )
        responses.get(
            url = 'https://api.pwnedpasswords.com/range/' + converted_pass2[:5],
            body= '000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n433F02071597741E6FF5A8EA34789ABBF43:11866',
            status=200
        )
        responses.get(
            url = 'https://api.pwnedpasswords.com/range/' + converted_pass3[:5],
            body= 'nB4AEDCB55F679D0F631B038F0B8BCE8B6FD:3\r\nB4F740E4FA23D2A771DAEA3EE818815A7EF:3\r\nB5B08BAE5A3B2DA90D3E70C52BA1BC88D6B:2\r\nB61552B10031A1C13A3247B5DBC89879A9E:7', # not included in the response body, in reality: B5CC17C8C093C015CCDB7E552AEE7911AA4:62063
            status=200
        )
        resulted_count = []
        for password in pass_list:
            count = conta_trapelate(pwned_API_check(password))
            resulted_count.append(count)
        self.assertEqual(resulted_count, [273646, 11866, 0]) 
        
    




if __name__ == '__main__':
    unittest.main()
