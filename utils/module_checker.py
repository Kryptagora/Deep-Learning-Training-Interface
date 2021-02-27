import importlib

'''
This file trys to load all needed Modules in order to run the programm,
if it fails, the programm wil not be executed.
'''

def check_modules():
    module_names = ['tkinter', 'PIL', 'numpy', 'torch', 'torchvision']

    for module in module_names:
        try:
            importlib.import_module(module)

        except ModuleNotFoundError:
            missing_module = '\x1b[1;32m' + module + '\x1b[0m'
            print(f'\x1b[1;31mModule {missing_module} \x1b[1;31mis not installed on your computer and is required to run this program.\x1b[0m')
            return False

    print('\x1b[1;32mDone!\x1b[0m')
    return True
