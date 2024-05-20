from Password_Checker.modules import manage_file as mf
from Password_Checker.modules import API_functions as api
from unittest import TestCase
from pathlib import Path
import os
import responses, hashlib
import unittest
import random
#print(cm.records[0]) -> stampa <LogRecord: root, 50, C:\Users\gioco\anaconda3\Lib\site-packages\Password_Checker\modules\manage_file.py, 26, "C:\Users\gioco\not_txt_file.docx is not a txt file">
#print(cm.output[0]) -> stampa il messaggio di log CRITICAL:root:C:\Users\gioco\not_txt_file.docx is not a txt file

class TestOnLogs_txt_to_list(TestCase):

    def test_LOGS_txt_to_list_not_txt_file(self): # TESTED OK 
        the_not_txt_file = Path.home() / 'not_txt_file.docx'
        content = 'password1\npassword2 password3'
        the_not_txt_file.parent.mkdir(exist_ok=True, parents=True)
        with open(the_not_txt_file, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        with self.assertLogs(level='CRITICAL', logger='root') as cm:
            mf.txt_to_list(the_not_txt_file)
        self.assertIn('not a txt file', cm.output[0]) 
        os.remove(the_not_txt_file)

    def test_LOGS_txt_to_list_empty_file(self): # 
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

    def test_txt_to_list_non_existing_file(self): # TEST
        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)
        with self.assertLogs(logger='root', level='ERROR') as cm:
            mf.txt_to_list(the_non_existing_file)
        self.assertIn(f'{str(the_non_existing_file)} not found', cm.output[0])
        
        
class Test_Logs_on_default_path(TestCase):
    def test_LOGS_default_file_path(self):
        with self.assertLogs(logger='root', level='INFO') as cm:
            mf.default_file_path()
        print(cm.output[0])
        self.assertIn('this is a default_path list of passwords', cm.output[0])

    def test_logs_default_file_path_overwrite(self):
        the_path = mf.default_file_path()
        content = ''
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write(content)
            f.close()
        with self.assertLogs(logger='root', level='WARNING') as cm:
            mf.default_file_path()
        
        self.assertIn(f'the file {the_path} is blank, then it will be overwritten', cm.output[0])
        
    def test_default_file_path_content_creation(self):  # TESTED OK 7°
        if os.path.exists(mf.default_file_path()):
            os.remove(mf.default_file_path())  
        with self.assertLogs(logger='root', level='DEBUG') as cm:
            mf.default_file_path()
        the_path = mf.default_file_path()
        self.assertIn(f'since {str(the_path)} is not found, it will be created', cm.output[1])
        

class Test_Logs_on_keep_passwords_safe(TestCase):

    def test_keep_passwords_safe_not_existing_file(self): # TESTED OK 
        the_non_existing_file = Path.home() / 'non_existing_file.txt'
        if os.path.exists(the_non_existing_file):
            os.remove(the_non_existing_file)
        with self.assertLogs(logger='root', level='ERROR') as cm:
            mf.keep_passwords_safe(the_non_existing_file)
        self.assertIn(f': file {str(the_non_existing_file)} not found', cm.output[0])
       

    def test_keep_passwords_safe_emptied(self):  # TESTED OK 9°
        the_path = mf.example_file()
        with open(the_path, 'w', encoding='utf-8') as f:
            f.write('password1\npassword2 password3')
            f.close()
        with self.assertLogs(logger='root', level='INFO') as cm:
            mf.keep_passwords_safe(the_path)
        self.assertIn('the note is now blank', cm.output[0])


@unittest.skip('skip')
class Test_Logs_on_API(TestCase):

    def test_richiedi_dati_API_error_4xx(self): # test the response type assertRaises or assertEqual depending on the type of response
        query = 'random' # fix using hash1[:5] as query
        converted_pass = hashlib.sha1(query.encode('utf-8')).hexdigest().upper()
        error_4xx = [400, 401, 403, 404]
        responses.get(
            url='https://api.pwnedpasswords.com/range/' + converted_pass[:5],
            # no text is required since the response raises an error
            status=random.choice(error_4xx)
        )
    
        with self.assertLogs() as cm:
            api.richiedi_dati_API(converted_pass[:5])
            pass
            
        print(cm.output)
        pass