import torch
import torch.nn as nn
import torch.nn.functional as F


class Model(nn.Module):

    def __init__(self) -> None:
        super().__init__()

        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=2, padding=1)  # 28 x 28 -> 14 x 14 x 16
        self.bn1 = nn.BatchNorm2d(16)

        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=2, padding=1) # 14 x 14 x 32 -> 7 x 7 x 32
        self.bn2 = nn.BatchNorm2d(32)

        self.fc1 = nn.Linear(32 * 7 * 7, 64)

        self.fc2 = nn.Linear(64, 10)


    def forward(self, x):
        x = self.bn1(self.conv1(x))
        x = F.relu(x)

        x = self.bn2(self.conv2(x))
        x = F.relu(x)

        x = torch.flatten(x, start_dim=1)

        x = self.fc1(x)
        x = F.relu(x)

        x = self.fc2(x)

        return x