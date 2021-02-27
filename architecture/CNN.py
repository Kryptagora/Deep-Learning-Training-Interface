import torch.nn as nn


class CNN(nn.Module):
    def __init__(self, out_labels:int=10):
        super(CNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(16),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5, stride=1, padding=2),
            nn.BatchNorm2d(32),
            nn.Dropout(p=0.2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.fc1 = nn.Linear(32*7*7, out_labels)

    def forward(self, x):
        # size from (1, 28, 28) to (16, 28, 28) to (16, 14, 14)
        x = self.layer1(x)
        # size from (16, 14, 14) to (32, 14, 14) to (32, 7, 7)
        x = self.layer2(x)
        x = x.reshape(x.size(0), -1)
        # output layer from 32*7*7 to 10 (num of labels)
        return self.fc1(x)
