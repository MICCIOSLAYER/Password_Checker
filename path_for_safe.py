def note_is_empty(path : str) -> bool:
    '''
    check if the note is blank
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
    '''
    with open(path, 'w', encoding='utf-8') as f:
        f.write('')
    print('the note is now blank, your passwords are safe')
    return None