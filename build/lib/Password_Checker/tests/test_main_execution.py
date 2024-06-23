import unittest
import responses
import hashlib

from Password_Checker.modules import main_execution


class Test_Successfull_main_execution_Module(unittest.TestCase):
    '''
    Test the right core_execution function in main_execution module
    ---------
    Given:
    - a list of passwords: ['hello', 'world', 'random']

    --------
    Methods: 
    - using the responses module to mock the request response one for each word

    ----------
    Expected:
    only expected_passwords_output  in output, if verbosity = False
    also expected_verbosity_output  in output, if verbosity = True
    '''
    @responses.activate
    def test_core_execution_True_verbosity(self):
        '''test the right functioning for a list of passwords'''
        query1 = 'hello'
        converted_pass1 = hashlib.sha1(
            query1.encode('utf-8')).hexdigest().upper()
        query2 = 'world'
        converted_pass2 = hashlib.sha1(
            query2.encode('utf-8')).hexdigest().upper()
        query3 = 'random'
        converted_pass3 = hashlib.sha1(
            query3.encode('utf-8')).hexdigest().upper()

        list_of_queries = [converted_pass1[:5],  # necessary for API_function module
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
        expected_passwords_output = ['hello has been hacked 273646 times',
                                     'world has been hacked 11866 times', 'random is not been hacked']
        expected_verbosity_output = '''For a better choise of your passwords, you can add some number and special caracters,
remember to always include both capital letter and lower letter, with at least of 8 characters.'''
        with self.assertLogs() as logs:
            main_execution.core_execution(pass_list, True)
            for printed_output in expected_passwords_output:
                self.assertIn(printed_output, logs.output)
            self.assertIn(expected_verbosity_output, logs.output)


if __name__ == "__main__":
    unittest.main()
