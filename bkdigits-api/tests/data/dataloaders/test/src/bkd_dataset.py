from torch.utils.data import Dataset

class UserDataset(Dataset):
    def __init__(self, data_path):
        super().__init__()
        self.data_path = data_path

    def collate(self, batch):
        return batch

    def __len__(self):
        return 0

    def __getitem__(self, index):
        return 0
