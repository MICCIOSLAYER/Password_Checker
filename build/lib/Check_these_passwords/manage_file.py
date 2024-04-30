import pathlib
from pathlib import Path
import os
import warnings

def txt_to_list(txt_file : pathlib.Path ) -> list: # FIXED
    '''
    get the path check if exists and return a list of passwords
    
    Parameters:
    path : str - the absolute-/path of the note to check
    '''
    assert txt_file.exists(), 'file not found'
    assert '.txt' in str(txt_file),  f'{txt_file} is not a txt file'
        
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            passwords_list = f.read().split()
            assert len(passwords_list) > 0, 'the note is blank, no passwords are stored here' # FIXME trasfrom it in a warning
            f.close()
            return passwords_list
    
    except FileNotFoundError:
        print(f'file {txt_file} not found')
        
    except SyntaxError as e:
        print(f'{e} in txt_to_list function')
     
            
def default_file_path() -> pathlib.Path: # FIXME introduce a if else and let the try with only syntax error, keep it simple with only 1 opening of the file.
    '''
    creation/ read of a file to read passwords by a default path in Desktop
    '''
    content = 'this@password is-s@f3 \nthan-this bla_bla@2023'
    desktop_path = pathlib.Path(os.path.expanduser("~/Desktop"))
    txt_file_default = desktop_path / 'default_list.txt'
    
# FIXME remove the default overwriting of the file

    try:  
        if os.path.exists(txt_file_default):  # if exists write it if blank
            with open(txt_file_default, 'r+', encoding='utf-8') as b: 
                if b.read() == '':  # to avoid the overwrite of the file if not empty
                    b.write(content)
                    print(f'this is a default_path list of passwords: {txt_file_default}')
                b.close()
            return (txt_file_default)
        else:   # if not exists create it
            with open(txt_file_default, 'w', encoding='utf-8') as f:
                f.write(content)
                f.close()
            #return absolute_default_path
        return (desktop_path / 'default_list.txt')
    except FileNotFoundError:
        print(f'file {txt_file_default} not found, choose another option')
    except SyntaxError as e:
        print(f'{e} in default_path function')
    

def keep_passwords_safe(txt_file : pathlib.Path) -> None:
    '''
    overwrite the file with a blanck note to keep safe your passrords

    Parameters:
    txt_file : Path - the absolute-/path of the note to overwrite
    '''
    assert txt_file.exists(), f'file{txt_file} not found, please be sure to insert the absolute path, in keep_passwords_safe function'
    try:        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write('')
            f.close()
            print('the note is now blank, your passwords are safe')
        return None
    except SyntaxError as e:
        print(f'{e} in keep_passwords_safe function')


def note_is_empty(path : pathlib.Path) -> bool:
    '''
    check if the note is blank

    Parameters:
    path : str - the absolute-/path of the note to check
    '''
    assert path.exists(), 'file not found'
    try:            
        txt_file = (path)
        absolute_txt_file = txt_file.resolve()
        assert absolute_txt_file.exists(), f'the path {absolute_txt_file} is incorrect'
        with open(path, 'r', encoding='utf-8') as f:
            if f.read() == '':
                print('the note is blank, no passwords are stored here')
                return True
        return False 
    except FileNotFoundError:
        print(f'file {path} not found')
    except SyntaxError as e:
        print(f'{e} in note_is_empty function')