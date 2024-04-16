#HACK use the pathlib to manage the path objects
import pathlib
def txt_to_list(path : str ) -> list:
    '''
    get the path check if exists and return a list of passwords
    
    Parameters:
    path : str - the absolute-/path of the note to check
    '''
    #txt_file = pathlib.Path(path) HACK?
    #while(txt_file.exists()):
    while True:
        try:
            txt_file = pathlib.Path(path)
            with open(txt_file, 'r', encoding='utf-8') as f:
                assert f.read() != '', 'the note is blank, no passwords are stored here'
                passwords_list = f.read().splitlines()

                return passwords_list
        
        except FileNotFoundError:
            print(f'file {path} not found')
            break
        except 
            
    pass


def note_is_empty(path : str) -> bool:
    '''
    check if the note is blank

    Parameters:
    path : str - the absolute-/path of the note to check
    '''
    with open(path, 'r', encoding='utf-8') as f: # TODO test the encoding
        if f.read() == '':
            print('the note is blank, no passwords are stored here')
            return True
        else:
            return False 

def overwrite_blanck_note(path : str) -> None:
    '''
    overwrite blank the note

    Parameters:
    path : str - the absolute-/path of the note to overwrite
    '''
    with open(path, 'w', encoding='utf-8') as f:
        f.write('')
    print('the note is now blank, your passwords are safe')
    return None