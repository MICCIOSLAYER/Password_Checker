#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

import unittest
import random
import responses
import hashlib
from Password_Checker.modules.API_functions import API_response, leaked_count, pwned_API_check


class Test_API_Module_right_work(unittest.TestCase):

    # TEST API_response-----------------------------------------------------
    @responses.activate
    def test_API_response_status_code(self):
        '''test status code 200
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        --------
        Methods:
        - using the responses lib to mock a requests to get a status_code of 200
        - using the API_response function to get the response
        ----------
        Expected Output:
        - expected the status_code to be 200
        '''
        query = 'hello'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',  # a part of the response.text
            status=200
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response.status_code, 200)

    @responses.activate
    # test the response type assertRaises or assertEqual depending on the type of response
    def test_API_response_content(self):
        '''
        Test content of a  response whose status_code is 200
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        --------
        Methods:
        - using the responses lib to mock a requests to get a status_code of 200
        - using the API_response function to get the response
        ----------
        Expected Output:
        - expected the response.text content to be the same in the 'body' of the mocked request
        '''
        query = 'hello'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',  # a part of the response.text
            status=200
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response.text, '000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646')

    # TEST leaked_count-----------------------------------------------------

    def test_non_zero_leaked_count(self):
        '''
        Test if the correct counts are returned,
        using leaked_count 
        ---------
        Given:
        - an hash to confront to the list of hashes, get it from the list itself
        - an object whose attribute .text give the text inside to act like as a mock response of a request
        -------
        Methods:
        - using the leaked_count function to get the count of violations
        ----------
        Expected Output:
        - expected the leaks to be 5
        '''
        class Response_text:
            def __init__(self, text='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646'):
                self.text = str(text)

        hashes = Response_text()
        hash5_to_check = '000AB2DEE342D579F6FE914C85B9CF98EDE'
        tuple_to_leaks = (hashes, hash5_to_check)
        self.assertEqual(leaked_count(tuple_to_leaks), 5)

    def test_leaked_count_zero(self):
        '''
        Test if the correct counts are returned,
        using leaked_count 
        ---------
        Given:
        - an hashe to confront to the list of hashes, one to get a null result
        - an object whose attribute .text give the text inside to act like as a mock response of a request
        -------
        Methods:
        - using the leaked_count function to get the count of violations
        ----------
        Expected Output:
        - expected the leaks to be 0
        '''
        class Response_text:
            def __init__(self, text='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646'):
                self.text = str(text)

        hashes = Response_text()
        # switched the last letter to get a null result
        hash5_to_check = '000AB2DEE342D579F6FE914C85B9CF98EDK'
        tuple_to_leaks = (hashes, hash5_to_check)
        self.assertEqual(leaked_count(tuple_to_leaks), 0)

    @responses.activate
    def test_leaked_count_higher_than_0(self):
        '''
        Test if the correct count (!=0) is returned,
        using leaked_count integrated with API_response
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        --------
        Methods:
        - using the responses lib to mock a requests to get the leaks
        - using the API_response function to get the response
        - using the leaked_count function to get the count of violations
        ----------
        Expected Output:
        - expected the leaks to be 273646
        '''

        query = 'hello'
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',  # a part of the response.text
            status=200
        )
        hashes = API_response(converted_pass[:5])

        hash_to_check = '61DDCC5E8A2DABEDE0F3B482CD9AEA9434D'
        tupla = (hashes, hash_to_check)
        leaks = leaked_count(tupla)
        self.assertEqual(leaks, 273646)

    @responses.activate
    def test_leaked_ZEROcount(self):
        '''
        Test if the correct count(==0) is returned, when not found        
        using leaked_count integrated with API_response
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        --------
        Methods:
        - using the responses lib to mock a requests to get the body
        - using the API_response function to get the response
        - using the leaked_count function to get the count of violations
        ----------
        Expected Output:
        - expected the leaks to be 0
        '''

        query = 'hello'
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',  # a part of the response.text
            status=200
        )

        hashes = API_response(converted_pass[:5])
        hash_to_check = '61DDCE5E8A2DABEDE0F3B482CD9AEA9434D'  # invented hash
        tupla = (hashes, hash_to_check)
        leaks = leaked_count(tupla)
        self.assertEqual(leaks, 0)

    @responses.activate
    def test_pwned_API_check_the_search_key(self):
        '''
        Test if the pwned_API_check return correspond to the return of API_response 
        and the preset hash '61DDCC5E8A2DABEDE0F3B482CD9AEA9434D'
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        - a mock object 
        --------
        Methods:
        - using the responses lib to mock a requests 
        - using the API_response function to get the response
        - using the pwned_API_check on the query to get the results to check
        ----------
        Expected Output:
        - expected the tuple to be composed of the API_response and the hash 61DDCC5E8A2DABEDE0F3B482CD9AEA9434D
        '''
        query = 'hello'
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',  # a part of the response.text
            status=200
        )
        resulted_tuple = pwned_API_check(query)
        expected_tuple = (API_response(
            converted_pass[:5]), '61DDCC5E8A2DABEDE0F3B482CD9AEA9434D')
        self.assertEqual(resulted_tuple[1], expected_tuple[1])

    @responses.activate
    def test_pwned_API_check_the_server_response(self):
        '''
        Test if the content of the response get from pwned_API_check is the same that the one get from API_response
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        - a mock object 
        --------
        Methods:
        - using the responses lib to mock a requests 
        - using the API_response function to get the response
        - using the pwned_API_check on the query to get the results to check
        ----------
        Expected Output:
        - expected the response content to be the same both in the API_response and the pwned_API_check

        '''
        query = 'hello'
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',  # a part of the response.text
            status=200
        )
        resulted_tuple = pwned_API_check(query)
        expected_tuple = (API_response(
            converted_pass[:5]), '61DDCC5E8A2DABEDE0F3B482CD9AEA9434D')
        self.assertEqual(resulted_tuple[0].content, expected_tuple[0].content)


class Test_API_Module_fails(unittest.TestCase):
    '''
    Test the response if the status code is a 4xx type
    ---------
    Given:
    - a query and its conversion in sha1 protocol
    - a mock object 
    --------
    Methods:
    - using the responses lib to mock a requests 
    - using the API_response function to get the response
    ----------
    Expected Output:
    - expected the response content to be the same of 'Client error'        
    '''

    @responses.activate
    def test_API_response_error_400(self):
        query = 'random'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response return an error
            status=400
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response, 'Client error')

    @responses.activate
    def test_API_response_error_401(self):
        query = 'random'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response return an error
            status=401
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response, 'Client error')

    @responses.activate
    def test_API_response_error_403(self):
        query = 'random'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response return an error
            status=403
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response, 'Client error')

    @responses.activate
    def test_API_response_error_404(self):
        query = 'random'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response return an error
            status=401
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response, 'Client error')

    @responses.activate
    # test the response type assertRaises or assertEqual depending on the type of response
    def test_API_response_error_429(self):
        query = 'random'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=429
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response, 'Client error')

    @responses.activate
    def test_API_response_error_503(self):
        '''
        Test the response if the status code is a 503 type
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        - a mock object 
        --------
        Methods:
        - using the responses lib to mock a requests 
        - using the API_response function to get the response
        ----------
        Expected Output:
        - expected the response content to be the same of 'Server error'        
        '''
        query = 'random'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=503
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response, 'Server error')

    @responses.activate
    def test_get_response_from_API_error_random_error(self):
        '''
        Test the response if the status code is a 303 type
        ---------
        Given:
        - a query and its conversion in sha1 protocol
        - a mock object 
        --------
        Methods:
        - using the responses lib to mock a requests 
        - using the API_response function to get the response
        ----------
        Expected Output:
        - expected the response.statuts_code to be 303
        '''
        query = 'hello'  # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(
            query.encode('utf-8')).hexdigest().upper()
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=303
        )
        response = API_response(converted_pass[:5])
        self.assertEqual(response.status_code, 303)


class Test_API_Module_combined(unittest.TestCase):

    @responses.activate
    def test_final_combination_API_functions_module(self):
        '''
        Test if the API_function.py module works well on a list of response 
        ---------
        Given:
        - three query and their conversion in sha1 protocol
        - three mock objects 
        --------
        Methods:
        - using the responses lib to mock the requests 
        - using the pwned_API_check on the query to get the response
        - using the leaked_count function to get the count of violations
        ----------
        Expected Output:
        - expected the list of count of violation to be the same of [273646, 11866, 0]

        '''
        query1 = 'hello'
        converted_pass1 = hashlib.sha1(
            query1.encode('utf-8')).hexdigest().upper()
        query2 = 'world'
        converted_pass2 = hashlib.sha1(
            query2.encode('utf-8')).hexdigest().upper()
        query3 = 'random'

        converted_pass3 = hashlib.sha1(
            query3.encode('utf-8')).hexdigest().upper()
        list_of_queries = [converted_pass1[:5],
                           converted_pass2[:5], converted_pass3[:5]]
        pass_list = [query1, query2, query3]

        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass1[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n61DDCC5E8A2DABEDE0F3B482CD9AEA9434D:273646',
            status=200
        )
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass2[:5],
            body='000AB2DEE342D579F6FE914C85B9CF98EDE:5\r\n003EC0930A89382B60E0C012A0F916AC33F:1\r\n0059D41E74575F8580A0687D1791E9B313F:23\r\n433F02071597741E6FF5A8EA34789ABBF43:11866',
            status=200
        )
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass3[:5],
            # not included in the response body, in reality: B5CC17C8C093C015CCDB7E552AEE7911AA4:62063
            body='nB4AEDCB55F679D0F631B038F0B8BCE8B6FD:3\r\nB4F740E4FA23D2A771DAEA3EE818815A7EF:3\r\nB5B08BAE5A3B2DA90D3E70C52BA1BC88D6B:2\r\nB61552B10031A1C13A3247B5DBC89879A9E:7',
            status=200
        )
        resulted_count = []
        for password in pass_list:
            count = leaked_count(pwned_API_check(password))
            resulted_count.append(count)
        self.assertEqual(resulted_count, [273646, 11866, 0])


if __name__ == '__main__':
    unittest.main()
