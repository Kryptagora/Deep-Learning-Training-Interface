from os.path import exists, join
import re

'''
This function checks if the filename is
(1) Valid and has no weird characters.
(2) Does not already exist in models.
'''

def check_filename(filename:str=None):
    default_dir = join('architecture', 'models')

    if not re.match("^[A-Za-z0-9_-]*$", filename):
        return False, 'The Modelname can only contain strings, letters, dashes and underlines!'

    savefile = join(default_dir, filename + '.ckpt')
    if exists(savefile):
        return False, 'The Modelname already exists! Choose a differnt name or delete the old one.'
    else:
        return True, savefile
