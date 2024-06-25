from Password_Checker.modules import manage_file as mf
from Password_Checker.modules import API_functions as api
from unittest import TestCase
from pathlib import Path
import os
import responses
import hashlib
import unittest
import random
# print(cm.records[0]) -> print <LogRecord: root, 50, C:\Users\gioco\anaconda3\Lib\site-packages\Password_Checker\modules\manage_file.py, 26, "C:\Users\gioco\not_txt_file.docx is not a txt file">
# print(cm.output[0]) -> print the log message.. CRITICAL:root:C:\Users\gioco\not_txt_file.docx is not a txt file


class TestOnLogs_txt_to_list(TestCase):

    def test_LOGS_txt_to_list_not_txt_file(self):
        '''
        Test log if the file passed is not a txt

        ---------
        Given:
        - a non blank file whose extension is not txt
        --------
        Methods:
        - txt_to_list function w the_not_txt_file as argument
        - using the context manager to write the_not_txt_file
        - using the assertLogs to catch all the logs in the output
        ----------
        Expected Output:
        - expected (not a txt file) at CRITICAL level of logs
        '''
        the_not_txt_file = Path.home() / 'not_txt_file.docx'
        content = 'password1\npassword 2\npassword3'
        the_not_txt_file.parent.mkdir(exist_ok=True, parents=True)
        with open(the_not_txt_file, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        with self.assertLogs(level='CRITICAL', logger='root') as cm:
            mf.txt_to_list(the_not_txt_file)
        self.assertIn('not a txt file', cm.output[0])
        os.remove(the_not_txt_file)

    def test_LOGS_txt_to_list_empty_file(self):
        '''
        Test logs if the file is empty
        ---------
        Given:
        - a blank txt file
        --------
        Methods:
        - txt_to_list function w the_empty_txt_file as argument
        - using the context manager to create a blank file:  the_empty_txt_file
        - using the assertLogs to catch all the logs in the output
        ----------
        Expected Output:
        - expected (no passwords are stored here) at WARNING level of logs
        '''
        the_empty_txt_file = Path.home() / 'the_empty_txt_file.txt'
        content = ''
        the_empty_txt_file.parent.mkdir(exist_ok=True, parents=True)
        with open(the_empty_txt_file, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        with self.assertLogs(logger='root', level='WARNING') as cm:
            mf.txt_to_list(the_empty_txt_file)
        self.assertIn('no passwords are stored here', cm.output[0])
        os.remove(the_empty_txt_file)

    def test_LOGS_txt_to_list_non_existing_file(self):
        '''
        Test logs when the path of file is not found, 
        when used the txt_to_list function
        ---------
        Given:
        - a variable of a file_path
        --------
        Methods:
        - using the context manager to create the_non_existing_file, then remove it
        - using the assertLogs to catch all the logs in the output
        ----------
        Expected Output:
        - expected (the_non_existing_file not found) at ERROR level in log's output
        '''
        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)
        with self.assertLogs(logger='root', level='ERROR') as cm:
            mf.txt_to_list(the_non_existing_file)
        self.assertIn(f'{str(the_non_existing_file)} not found', cm.output[0])


class Test_Logs_on_default_path(TestCase):
    def test_LOGS_default_file_path(self):
        '''
        Test logs when executing derault_file_path

        ---------
        Given:
        - just execute the default_file_path()
        --------
        Methods:
        - execute the default_file_path function to get an output
        - using the assertLogs to catch all the logs in the output
        ----------
        Expected Output:
        - expected (this is a default_path list of passwords) at DEBUG level of logs
        '''
        with self.assertLogs(logger='root', level='DEBUG') as cm:
            mf.default_file_path()
        print(cm.output[0])
        self.assertIn('this is a default_path list of passwords', cm.output[0])

    def test_logs_default_file_path_overwrite(self):
        '''
        Test logs when overwriting the default_path file if this is blank
        ---------
        Given:
        - a blank file
        --------
        Methods:
        - using the default_file_path, the file is created
        - using the contex manager it is overwrite with (''), then execute again the default_file_path
        ----------
        Expected Output:
        - expected (the file 'at default_path' is blank, then it will be overwritten) at WARNING level of log's output
        '''
        the_path = mf.default_file_path()
        content = ''
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        with self.assertLogs(logger='root', level='WARNING') as cm:
            mf.default_file_path()
        self.assertIn(
            f'the file {the_path} is blank, then it will be overwritten', cm.output[0])

    def test_default_file_path_content_creation(self):
        '''
        Test logs for the creation of the default file path,
        when it not exists yet
        ---------
        Given:
        - nothing
        --------
        Methods:
        - using the context manager remove the default_file_path if it already exists, then execute the default_file_path() function again
        - using the assertLogs to catch all the logs in the output
        ----------
        Expected Output:
        - expected (since 'the default path' is not found, it will be created) at DEBUG level of logs
        '''
        if os.path.exists(mf.default_file_path()):
            os.remove(mf.default_file_path())
        with self.assertLogs(logger='root', level='DEBUG') as cm:
            mf.default_file_path()
        the_path = mf.default_file_path()
        self.assertIn(
            f'since {str(the_path)} is not found, it will be created', cm.output[1])


class Test_Logs_on_keep_passwords_safe(TestCase):

    def test_keep_passwords_safe_not_existing_file(self):
        '''
        Test logs if the file is not found, when is supposed to be
        overwrited by a blank one
        ---------
        Given:
        - a file path to the non_existing_file.txt file
        --------
        Methods:
        - using the context manager to remove the file, before the execution of keep_passwords_safe()
        - using the assertLogs to catch all the logs in the output
        ----------
        Expected Output:
        - expected (file 'the_non_existing_file path' not found) at ERROR level of logs
        '''
        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)
        with self.assertLogs(logger='root', level='ERROR') as cm:
            mf.keep_passwords_safe(the_non_existing_file)
        self.assertIn(
            f': file {str(the_non_existing_file)} not found', cm.output[0])

    def test_keep_passwords_safe_emptied(self):
        '''
        Test logs of keep_passwords_safe, if the file is empty
        ---------
        Given:
        - the example_file path from example_file() function
        --------
        Methods:
        - using the context manager to overwrite the file with a random content
        - using the assertLogs to catch all the logs in the output
        ----------
        Expected Output:
        - expected (the note is now blank) at INFO level of logs
        '''
        the_path = mf.example_file()
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write('password1\npassword 2\npassword3')
            f.close()
        with self.assertLogs(logger='root', level='INFO') as cm:
            mf.keep_passwords_safe(the_path)
        self.assertIn('the note is now blank', cm.output[0])


if __name__ == '__main__':
    unittest.main()
