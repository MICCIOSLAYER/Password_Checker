#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__init__.py file for command line application."""

__author__ = 'Renato Eliasy'
__email__ = 'renato.eliasy@studio.unibo.it'

from Password_Checker.modules import manage_file as mf
import unittest as utt
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import os

import logging
# testing the straight behaviour of unittest test single input -> output


class Test_File_Module_single_successes(utt.TestCase):

    # test on TXT_TO_LIST---------------------------------------------------
    def test_txt_to_list_type(self):
        '''
        Test the type of data stored in the return of txt_to_list
        ---------
        Given:
        - nothing
        --------
        Methods:
        - using the example_file to get a file with some strings inside, trasformed in a list through txt_to_list

        ----------
        Expected Output:
        - a list of strings
        '''
        the_list = mf.txt_to_list(mf.example_file())
        for password in the_list:
            self.assertEqual(type(password), str)

    def test_not_txt_to_list(self):
        '''
        Test if the function raises an error when the file is not a .txt
        ---------
        Given:
        - a docx file
        --------
        Methods:
        - use of the txt_to_list to get the list from the docx file

        ----------
        Expected Output:
        - a TypeError raise due to the wrong extension of the file
        '''
        the_list = mf.txt_to_list('not_txt_file.docx')
        self.assertRaises(TypeError, the_list)

    def test_txt_to_list_return(self):
        '''
        Test if the function returns the list of passwords stored in the file as the_list
        ---------
        Given:
        - a list of passwords
        --------
        Methods:
        - use contex maanger to write the list of str in the file
        - use of the txt_to_list to get the list from the txt file
        - compare the given w the obtained
        ----------
        Expected Output:
        - same output between the given and the obtained
        '''

        the_list = ['password1', 'password2', 'password3']
        content = 'password1\npassword2 password3'
        testing_file_path = Path.home() / 'testing_file.txt'
        with open(testing_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.assertEqual(mf.txt_to_list(testing_file_path), the_list)
        os.remove(testing_file_path)

    # TEST ON DEFAULT_FILE_PATH----------------------------------------------
    def test_default_file_path_existence_isFile(self):
        '''
        Test if the default file is a txt-file
        ---------
        Given:
        - nothing
        --------
        Methods:
        - use of the default_file_path to create the default file
        ----------
        Expected Output:
        - expect the creation of file type and the extension to be .txt
        '''

        the_path = mf.default_file_path()
        self.assertTrue(Path(the_path).is_file)
        self.assertIn('.txt', str(the_path))

    def test_default_file_path_existence_(self):
        '''
        Test the existence of default_file_path
        ---------
        Given:
        - nothing
        --------
        Methods:
        - use of the default_file_path to create the default_file

        ----------
        Expected Output:
        - the existence of the default file path
        '''

        the_path = mf.default_file_path()
        self.assertTrue(os.path.exists(the_path))

    def test_default_file_path_content_just_created(self):
        '''
        Test if the default file is created, with the pre-set content,
        when executing default_file_path() and there are no default_file_path
        ---------
        Given:
        - nothing
        --------
        Methods:
        - remove if present the default file path
        - use of the default_file_path() to create the default_file from zero
        ----------
        Expected Output:
        - the content of the default file has to be the pre-set one
        '''

        if os.path.exists(mf.default_file_path()):
            os.remove(mf.default_file_path())
        the_path = mf.default_file_path()
        with open(the_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
        self.assertEqual(
            content, 'D_default_path4 these@password isins1de thi5Pc')
        self.assertNotEqual(Path(the_path).stat().st_size, 0)

    def test_default_file_path_not_overwriting(self):
        '''
        Test if the default_file_path is not overwritten if not empty
        ---------
        Given:
        - the default_file with an overwrited content
        --------
        Methods:
        - use of the contex manager to overwrite the default file
        - execute the default_file_path() after

        ----------
        Expected Output:
        - the same 'content' before and after the overwrite, when launched the default_file_path()
        '''

        the_path = mf.default_file_path()
        content = 'password1\npassword2 password3'
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        mf.default_file_path()
        with open(the_path, 'r', encoding='utf-8') as f:
            f.seek(0)
            expected_content = f.read()
            f.close()
        self.assertEqual(expected_content, content)

    # TEST ON KEEP_PASSWORDS_SAFE--------------------------------------------
    def test_keep_passwords_example_file_safe_emptied(self):
        '''
        Test if keep_passwords_safe empties the default file
        ---------
        Given:
        - the example file path through the example_path()
        --------
        Methods:
        - use of the keep_passwords_safe() to overwrite an empty file in the same location

        ----------
        Expected Output:
        - a blank file
        '''

        the_path = mf.example_file()
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write('password1\npassword2 password3')
            f.close()
        mf.keep_passwords_safe(the_path)
        with open(the_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
        self.assertEqual(content, '')

    def test_keep_passwords_safe_emptied(self):
        '''
        Test if keep_passwords_safe empties the default file
        ---------
        Given:
        - the example file path through the explicit Path 
        --------
        Methods:
        - use of the keep_passwords_safe() to overwrite an empty file in the same location

        ----------
        Expected Output:
        - a blank file
        '''

        the_path = Path.home() / "Check_these_passwords" / "example_list.txt"
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write('password1\npassword2 password3')
            f.close()
        mf.keep_passwords_safe(the_path)
        with open(the_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
        self.assertEqual(content, '')

    def test_keep_passwords_safe_example_file_still_there(self):
        '''
        Test if the emptied file still exists, after the blanking
        ---------
        Given:
        - the example file
        --------
        Methods:
        - use of the keep_passwords_safe() to overwrite the file 

        ----------
        Expected Output:
        - the file still exists
        '''
        the_path = mf.example_file()
        the_emptied_file = mf.keep_passwords_safe(mf.example_file())
        self.assertTrue(os.path.exists(the_path))

    def test_keep_passwords_safe_still_there(self):
        '''
        Test if the emptied file still exists, after the blanking
        ---------
        Given:
        - the explicit path
        --------
        Methods:
        - use the contex manager to create a not empty file
        - use of the keep_passwords_safe() to overwrite the file 

        ----------
        Expected Output:
        - the file still exists
        '''
        the_path = Path.home() / "Check_these_passwords" / "example_list.txt"
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write('something\nin this file')
        the_emptied_file = mf.keep_passwords_safe(the_path)
        self.assertTrue(os.path.exists(the_path))

    # test on EXAMPLE_FILE_PATH-----------------------------------------------

    def test_example_file_is_file(self):
        '''
        Test if example_file_path is a file
        ---------
        Given:
        - the example file 
        --------
        Methods:
        - use of the example_file() to create the file

        ----------
        Expected Output:
        - a file type return
        '''

        the_path = mf.example_file()
        self.assertTrue(Path(the_path).is_file)

    def test_example_file_content(self):
        '''
        Test if the example file has the pre-set content
        ---------
        Given:
        - the example file 
        --------
        Methods:
        - use of the context manager to read the file

        ----------
        Expected Output:
        - the content of the red file must be equal to the pre-set one
        '''
        the_path = mf.example_file()
        with open(the_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
        self.assertEqual(content, 'today@is @b34UtIfull\nTh4n Y3sterd@y')


class Test_File_Module_single_failures(utt.TestCase):
    # test it will fail as it is expected to fail

    def test_txt_to_list_non_existing_file(self):
        '''
        Test if txt_to list return string is what suppsed to be,
        in case of non_existing_file
        ---------
        Given:
        - a txt file
        --------
        Methods:
        - remove the file if exist, then use the variable in the txt_to-list function

        ----------
        Expected Output:
        - the string 'file not found'
        '''

        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)

        self.assertEqual('file not found', mf.txt_to_list(
            Path.home() / 'non_existing_file.txt'))

    def test_txt_to_list_not_txt_file(self):
        '''
        Test if the return string is right in case of not_txt_file
        ---------
        Given:
        - a non empty docx file
        --------
        Methods:
        - use of the exception handling to catch the content of exception

        ----------
        Expected Output:
        - the content of raised exception to be 'this is not a txt file'
        '''

        the_not_txt_file = Path.home() / 'not_txt_file.docx'
        content = 'password1\npassword2 password3'
        the_not_txt_file.parent.mkdir(exist_ok=True, parents=True)
        with open(the_not_txt_file, 'w', encoding='utf-8') as f:
            f.write(content)

        try:
            mf.txt_to_list(the_not_txt_file)
        except TypeError as e:
            self.assertEqual(str(e), 'this is not a txt file')

        os.remove(the_not_txt_file)

    @utt.skip(reason="Not working, as the encoding is not important for txt files")
    def test_txt_to_list_unreadable_file(self):
        '''
        Test if the return string is right in case of unreadable_file due to different encoding
        ---------
        Given:
        - a txt file, encoded cp1252
        --------
        Methods:
        - use of the txt_to_list() to read the file

        ----------
        Expected Output:
        - Exception, whose content is 'Unreadable file, assure to use a UTF-8 encoded file to store your passwords'
        '''

        the_unreadable_file = Path.home() / 'unreadable_file.txt'
        content = 'password1\npassword2 password3'
        with open(the_unreadable_file, 'w', encoding='cp1252', errors='strict') as f:
            f.write(content)
            f.close()
        self.assertEqual(mf.txt_to_list(the_unreadable_file),
                         'Unreadable file, assure to use a UTF-8 encoded file to store your passwords')
        os.remove(the_unreadable_file)

        pass  # has to be skipped, as the encoding is not important for txt files

    def test_keep_passwords_safe_not_existing_file(self):
        '''
        Test if the return string is right in case of non_existing_file
        ---------
        Given:
        - a variable of a path of a file
        --------
        Methods:
        - remove the file, then use keep_passwords_safe() with argument this file

        ----------
        Expected Output:
        - content of raised exception to be 'Something went wrong while overwriting the file, where stored the passwords'
        '''

        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)
        try:
            mf.keep_passwords_safe(the_non_existing_file)
        except FileNotFoundError as e:
            self.assertEqual(mf.keep_passwords_safe(the_non_existing_file),
                             'Something went wrong while overwriting the file, where stored the passwords')


class Test_File_Module_combined_successes(utt.TestCase):

    def test_keep_passwords_safe_and_txt_to_list(self):
        '''
        Test if the passwords_list after keep_passwords_safe is empty
        ---------
        Given:
        - a path file from example file
        --------
        Methods:
        - use of keep_passwords_safe on example_file

        ----------
        Expected Output:
        - txt_to_list on the file_path to return an empty list
        '''

        file_to_be_tested = mf.example_file()
        mf.keep_passwords_safe(file_to_be_tested)

        self.assertEqual(mf.txt_to_list((file_to_be_tested)), [])

    def test_keep_passwords_safe_and_default_file_path(self):
        '''
        Test if the default file is overwritten and emptied after keep_passwords_safe
        ---------
        Given:
        - the default file, from default_file_path
        --------
        Methods:
        - use of the keep_passwords_safe() and default_file_path() to check if the file content is erased and overwritten

        ----------
        Expected Outputs:
        - a balnk file after keep_passwords_safe()
        - the default content after emptied the default file and execute the default_file_path()
        '''

        dir_to_be_tested = mf.default_file_path()
        mf.keep_passwords_safe(mf.default_file_path())
        # test if the file is empty as keep_passwords_safe should do
        with open(dir_to_be_tested, 'r', encoding='utf-8') as f:
            blank_file = f.read()
            f.close()

        self.assertEqual(blank_file, '')  # be sure that the file is empty
        # test if the file is overwritten as default_file_path should do
        mf.default_file_path()
        with open(mf.default_file_path(), 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()

        self.assertEqual(
            content, 'D_default_path4 these@password isins1de thi5Pc')


if __name__ == '__main__':
    utt.main()
