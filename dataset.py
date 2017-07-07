import os

import numpy as np

import cv2
import torch
import torchvision.datasets as dset
import torchvision.transforms as transforms
from lsun_room import Dataset, Phase


class ImageFolderDataset(dset.ImageFolder):

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    def __init__(self, root, target_size, phase=Phase.TRAIN):
        self.target_size = target_size
        self.dataset = Dataset(root_dir=root, phase=phase)
        self.filenames = [e.name for e in self.dataset.items]

    def __getitem__(self, index):
        return self.load(self.filenames[index])

    def load(self, name):
        image_path = os.path.join(self.dataset.image, '%s.jpg' % name)
        label_path = os.path.join(self.dataset.layout_image, '%s.png' % name)

        img = cv2.imread(image_path)
        lbl = cv2.imread(label_path, 0)

        img = cv2.resize(img, self.target_size, cv2.INTER_LINEAR)
        lbl = cv2.resize(lbl, self.target_size, cv2.INTER_NEAREST)

        img = self.transform(img)
        lbl = np.clip(lbl, 1, 5) - 1
        lbl = torch.from_numpy(np.expand_dims(lbl, axis=0)).long()

        return img, lbl

    def __len__(self):
        return len(self.filenames)
