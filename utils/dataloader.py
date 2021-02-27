from torch.utils.data import DataLoader, Dataset
from torchvision import datasets, transforms
import sys
sys.path.append('..')


def load_data(batch_size:int = 100, root_folder:str='data', dataset:str='MNIST'):
    transform = transforms.Compose([transforms.ToTensor()])
    if dataset == 'EMNIST':
        # train every letter and digit ('byclass')
        trainset = datasets.EMNIST(root=root_folder, split='byclass', train=True, download=True, transform=transform)
        testset = datasets.EMNIST(root=root_folder, split='byclass', train=False, download=True, transform=transform)

    elif dataset == 'MNIST':
        # train only letters ('byclass')
        trainset = datasets.EMNIST(root=root_folder, split='digits', train=True, download=True, transform=transform)
        testset = datasets.EMNIST(root=root_folder, split='digits', train=False, download=True, transform=transform)


    train_loader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(trainset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader
