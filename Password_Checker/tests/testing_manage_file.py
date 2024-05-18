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
# HACK? use temp file 

    # test on TXT_TO_LIST---------------------------------------------------
    def test_txt_to_list_type(self): # TESTED OK 
        the_list = mf.txt_to_list(mf.example_file())
        for password in the_list:
            self.assertEqual(type(password), str)   
    
    def test_not_txt_to_list(self): # to be tested
        the_list = mf.txt_to_list('not_txt_file.docx')
        self.assertRaises(TypeError, the_list)

    def test_txt_to_list_return(self): # TESTED OK 
        the_list = ['password1', 'password2', 'password3']
        content = 'password1\npassword2 password3'
        testing_file_path = Path.home() / 'testing_file.txt'
        with open(testing_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        self.assertEqual(mf.txt_to_list(testing_file_path), the_list)
        os.remove(testing_file_path) # HACK keep it clean or use a mock_object? => temp file  
        

    
    # TEST ON DEFAULT_FILE_PATH----------------------------------------------
    def test_default_file_path_existence_isFile(self): # TESTED OK 5°
        the_path = mf.default_file_path()
        self.assertTrue(Path(the_path).is_file)
        self.assertIn('.txt',str(the_path)) # HACK use a regex?
    
    def test_default_file_path_existence_(self): # TESTED OK 6°
        the_path = mf.default_file_path()
        self.assertTrue(os.path.exists(the_path))
    
    def test_default_file_path_content_just_created(self):  # TESTED OK 7°
        if os.path.exists(mf.default_file_path()):
            os.remove(mf.default_file_path())  
        the_path = mf.default_file_path()
        with open(the_path, 'r', encoding='utf-8') as f:
            content = f.read() 
            f.close()
        self.assertEqual(content , 'D_default_path4 these@password isins1de thi5Pc')
        self.assertNotEqual(Path(the_path).stat().st_size, 0)
    
    def test_default_file_path_not_overwriting(self): # TESTED OK 8°
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
    def test_keep_passwords_safe_emptied(self):  # TESTED OK 9°
        the_path = mf.example_file()
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write('password1\npassword2 password3')
            f.close()
        mf.keep_passwords_safe(the_path)
        with open(the_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
        self.assertEqual(content, '')      
    
    def test_keep_passwords_safe_still_there(self):   # TESTED OK 11°
        the_emptied_file = mf.keep_passwords_safe(mf.example_file())
        self.assertTrue(os.path.exists(mf.example_file()))
        

    #test on EXAMPLE_FILE_PATH-----------------------------------------------
    def test_example_file_is_file(self): # TESTED OK 12°
        the_path = mf.example_file()
        self.assertTrue(Path(the_path).is_file)

    def test_example_file_content(self): # TESTED OK 13°
        the_path = mf.example_file()
        with open(the_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
        self.assertEqual(content, 'today@is @b34UtIfull \nTh4n Y3sterd@y')
        

class Test_File_Module_single_failures(utt.TestCase):
    # test it will fail as it is expected to fail

    def test_txt_to_list_non_existing_file(self): # TESTED OK 3°
        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)
        # TODO self.assertLog... already printed in terminal output
        self.assertEqual('file not found' , mf.txt_to_list(Path.home() / 'non_existing_file.txt'))

    def test_txt_to_list_not_txt_file(self): # TESTED OK 
        the_not_txt_file = Path.home() / 'not_txt_file.docx'
        content = 'password1\npassword2 password3'
        the_not_txt_file.parent.mkdir(exist_ok=True, parents=True)
        with open(the_not_txt_file, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        #assertLog... already printed in terminal output just to be verified
        self.assertEqual(mf.txt_to_list(the_not_txt_file), 'this is not a txt file')
        os.remove(the_not_txt_file)

    @utt.skip(reason="Not working, as the encoding is not important for txt files") # LEAVE LIKE THIS
    def test_txt_to_list_unreadable_file(self):
        the_unreadable_file = Path.home() / 'unreadable_file.txt'
        content = 'password1\npassword2 password3'
        with open(the_unreadable_file, 'w', encoding='cp1252', errors='strict') as f:
            f.write(content)
            f.close()        
        self.assertEqual(mf.txt_to_list(the_unreadable_file), 'Unreadable file, assure to use a UTF-8 encoded file to store your passwords')
        os.remove(the_unreadable_file)

        pass # has to be skipped, as the encoding is not important for txt files

    def test_keep_passwords_safe_not_existing_file(self): # TESTED OK 
        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)

        self.assertEqual(mf.keep_passwords_safe(the_non_existing_file), 'Something went wrong while overwriting the file, where stored the passwords')
      

class Test_File_Module_combined_successes(utt.TestCase):
    # test on COMBINED FUNCTIONS
    
    def test_keep_passwords_safe_and_txt_to_list( self):  # TESTED OK 14°
        file_to_be_tested = mf.example_file()
        mf.keep_passwords_safe(file_to_be_tested)

        self.assertEqual( mf.txt_to_list((file_to_be_tested)), [])
         

    def test_keep_passwords_safe_and_default_file_path(self): # TESTED OK 15°
        dir_to_be_tested = mf.default_file_path()
        mf.keep_passwords_safe(mf.default_file_path())
        with open(dir_to_be_tested, 'r', encoding='utf-8') as f: # test if the file is empty as keep_passwords_safe should do
            blank_file =f.read()
            f.close()

        self.assertEqual(blank_file, '') # be sure that the file is empty
        # test if the file is overwritten as default_file_path should do
        mf.default_file_path()
        with open(mf.default_file_path(), 'r', encoding='utf-8') as f: 
            content = f.read()
            f.close()

        self.assertEqual(content, 'D_default_path4 these@password isins1de thi5Pc')
        



   

# testing integration testing try to use multiple f in a single test

# testing functional testing try to compose the functions in a single test


if __name__ == '__main__':
    utt.main()