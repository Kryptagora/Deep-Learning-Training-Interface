import torch
import sys
sys.path.append('..')

'''
This function loads a model and uses it for prediction.
'''


def predict(main_window=None, drawed_picture=None, modelname:str=None):
    try:
        model = torch.load(f'architecture/models/{modelname}')
    except:
        return main_window.set_warn('Model cant be loaded, it does not exist!')

    model.eval()
    #model.float()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    data_np = drawed_picture / 255
    data_np = data_np.reshape(1,1,28,28)



    tensor = torch.from_numpy(data_np)
    output = model(tensor.float().to(device))

    mapping = {}
    with open('utils/emnist-balanced-mapping.txt', 'r') as fh:
        for line in fh.readlines():
            label, char = line.split(' ')
            mapping[int(label)] = chr(int(char))

    return mapping[output.argmax(1).item()]
