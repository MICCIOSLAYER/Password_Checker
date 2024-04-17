import pathlib
def txt_to_list(path : str ) -> list:
    '''
    get the path check if exists and return a list of passwords
    
    Parameters:
    path : str - the absolute-/path of the note to check
    '''

    #txt_file = pathlib.Path(path) HACK?
    #while('txt' in path):
    try:
        txt_file = pathlib.Path(path)
        absolute_txt_file = txt_file.resolve()
        #assert absolute_txt_file.exists(), 'file not found'
        with open(absolute_txt_file, 'r', encoding='utf-8') as f:
            assert f.read() != '', 'the note is blank, no passwords are stored here'
            passwords_list = f.read().splitlines()
            f.close()

            return passwords_list
    
    except FileNotFoundError:
        print(f'file {path} not found')
        
    except SyntaxError as e:
        print(f'{e} in txt_to_list function')
     
            
    pass

def keep_passwords_safe(path : str) -> None:
    '''
    overwrite the file with a blanck note to keep safe your passrords

    Parameters:
    path : str - the absolute-/path of the note to overwrite
    '''
    assert path.exists(), f'file{path} not found in keep_passwords_safe function'
    try:            
        txt_file = pathlib.Path(path)
        absolute_txt_file = txt_file.resolve()
        assert absolute_txt_file.exists(), f'file{absolute_txt_file} not found in keep_passwords_safe function'
        
        with open(absolute_txt_file, 'w', encoding='utf-8') as f:
            f.write('')
            f.close()
        with open(absolute_txt_file, 'r', encoding='utf-8') as w: 
            if w.read() == '':
                print('the note is now blank, your passwords are safe')
        return None
    except SyntaxError as e:
        print(f'{e} in keep_passwords_safe function')


def note_is_empty(path : str) -> bool:
    '''
    check if the note is blank

    Parameters:
    path : str - the absolute-/path of the note to check
    '''
    assert path.exists(), 'file not found'
    try:            
        txt_file = pathlib.Path(path)
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

'''
def overwrite_blanck_note(path : str) -> None:
    
    overwrite blank the note

    Parameters:
    path : str - the absolute-/path of the note to overwrite
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write('')
    print('the note is now blank, your passwords are safe')
    return None
    '''