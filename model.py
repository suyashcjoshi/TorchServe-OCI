import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.pool2 = nn.MaxPool2d(2)
        self.pool3 = nn.MaxPool2d(3)

        # 3 x 224 x 224
        self.conv1 = nn.Conv2d(3, 10, 3) # 222
        # pool2 111
        self.conv2 = nn.Conv2d(10, 16, 4) # 108
        self.conv2_bn = nn.BatchNorm2d(16)
        # pool2 54
        self.conv3 = nn.Conv2d(16, 20, 5) # 50
        self.conv3_bn = nn.BatchNorm2d(20)
        # pool2 25
        self.conv4 = nn.Conv2d(20, 20, 5) # 21
        self.conv4_bn = nn.BatchNorm2d(20)
        # pool3 7

        self.fc1 = nn.Linear(20 * 7 * 7, 10)
        self.fc2 = nn.Linear(10, 2)

    def forward(self, x):

        x = self.pool2(F.relu(self.conv1(x)))
        x = self.pool2(F.relu(self.conv2_bn(self.conv2(x))))
        x = self.pool2(F.relu(self.conv3_bn(self.conv3(x))))
        x = self.pool3(F.relu(self.conv4_bn(self.conv4(x))))

        x = x.view(-1, 20 * 7 * 7)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
