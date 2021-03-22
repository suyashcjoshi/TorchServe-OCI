import os
from skimage import io, transform
import numpy as np
import torch
from torch.utils.data import Dataset

class DogsCatsDataset(Dataset):
    """Dogs/Cats dataset."""

    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (string): Directory with all the images.
            transorm (callable, optional): Optional transform to apply
                to samples
            training (boolean): If False, __getitem__ returns additional
                metadata

        Dataset Sample:
            {
                'image':
                'label': 0/1
            }
        Dogs are ones, Cats are zeros
        """
        self.filenames = os.listdir(root_dir)
        self.root_dir = root_dir
        self.transform = transform

    def show_item(self, idx):
        import matplotlib.pyplot as plt
        sample = self.__getitem__(idx)

        plt.title(sample['path'])
        img = sample['image'].numpy().transpose((1, 2, 0))
        img = img / 2 + 0.5
        plt.imshow(img)
        plt.show()

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        img_path = os.path.join(self.root_dir, self.filenames[idx])
        img_type = 1 if self.filenames[idx][:3] == 'dog' else 0
        image = io.imread(img_path)

        if self.transform:
            image = self.transform(image)

        sample = {'image': image, 'label': img_type, 'path': img_path}

        return sample
