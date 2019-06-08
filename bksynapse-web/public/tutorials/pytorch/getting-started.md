# Get Started with BK.Synapse & PyTorch
This tutorial will help you get started with our PyTorch computational backend. If you're not familiar with PyTorch, the PyTorch [home page](https://pytorch.org/tutorials/) offers some excellent tutorials for beginners.

In this tutorial, we will train a simple 2-layer convolutional network on the MNIST dataset.

## Prepare your dataset
Torchvision (PyTorch's official CV helper library) offers convenient classes for standard datasets, MNIST included. We'll make use of this by writing a Data Loader that wraps MNIST. Create a file called `bks_dataset.py` with the following contents:

```py

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
```

We defined 2 classes, `UserDataset` and `UserValDataset`. Note that the class names and filename cannot be changed, as they are used as entrypoints for BK.Synapse. As their names imply, `UserDataset` is used for loading training data, while `UserValDataset` is used for loading validation data.

FOr convenience, we set `download=True`, which means the datasets are automatically downloaded if needed. This can cause a delay of several minutes (depending on your network speed) on your first run.

With `bks_dataset.py` created, compress the file into a zip file, then upload it in BK.Synapse's `Data Loaders/Create` page.

We still need an empty Dataset for MNIST to be downloaded into. Create one in `Datasets/Create`.

## Prepare the model
Next, we'll prepare our convolutional network. Create a file called `bks_model.py` with the following contents:

```py

import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return x


class UserModel(Net):
    def loss(self, output, target):
        return F.cross_entropy(output, target, reduction='mean')

    def metrics(self, output, target):
        preds = torch.argmax(output, dim=1)
        total = preds.shape[-1]
        correct = (preds == target).float()
        acc = torch.sum(correct) / total
        return {
            'accuracy': acc.item()
        }
```

2 classes are defined in `bks_dataset.py`. The `Net` class is a standard PyTorch module with 2 Convolution layers, a 2D Dropout layer and 2 Linear (feedforward) layers with ReLu activation. `UserModel` is a required entrypoint that wraps `Net` and implements the `loss()` and `metrics()` methods to be calculated during training.

With `bks_model.py` created, compress the file into a zip file, then upload it in BK.Synapse's `Models/Create` page.

## Job configuration
We've finished the 3 building blocks for our training pipeline. Let's create a Job to put them all together. Go to `Jobs/Create` and select your created components for the Job. You may also want to specify training parameters. Since this is a tiny dataset on a small network, we recommend a batch size of 32-64, a learning rate 0f 0.001 and 10 total epochs.

Once all configuration is complete, select `Create and Run`.

## Monitor your Job
When selecting `Create and Run`, you'll be taken to the `Jobs/Manage` screen. Your Job should be in the SETUP state before transitioning to TRAINING. You can view the training progress, as well as the loss and metrics values (as previously defined in `bks_model.py`) on the UI.

The Job should finish shortly with a validation accuracy of roughly 95%.

## Viewing results
Once your Job finishes, you can view results and analytics in the corresponding page (look in the Job's &#8942; section). Here, you can view metrics on each epochs, analyze training time, and download snapshots for further use.

Congrats, you've successfully achieved 90% accuracy on MNIST with BK.Synapse. Of course, that was quite a simple example that didn't touch on some of the framework's nuances. See our other tutorials for more details.
