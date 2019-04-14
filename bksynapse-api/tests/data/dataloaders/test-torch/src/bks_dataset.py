from torch.utils.data import Dataset
from torchvision.datasets import MNIST
from torch.utils.data.dataloader import default_collate
from torchvision import transforms

class UserDataset(MNIST):
    def __init__(self, data_path):
        super().__init__(data_path, train=True, 
            download=True, transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ]))

    def collate(self, batch):
        return default_collate(batch)


class UserValDataset(MNIST):
    def __init__(self, data_path):
        super().__init__(data_path, train=False, 
            download=True, transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
            ]))

    def collate(self, batch):
        return default_collate(batch)
