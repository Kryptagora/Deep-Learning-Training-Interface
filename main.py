from interface.main_window import DrawAndPredict
from utils.module_checker import check_modules

_version_ = '1.1.0'

if __name__ == "__main__":
    print(f'Welcome to DLTI v{_version_}!')
    print(f'Checking Modules...')
    if not check_modules():
        quit()

    title = 'Deep Learning Training Interface'
    App = DrawAndPredict(title)
