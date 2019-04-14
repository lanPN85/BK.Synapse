# Welcome to the BK.Synapse Docs

&nbsp;

BK.Synapse is a tool that can help you effortlessly train Deep Learning models on multiple devices, with minimal changes to your existing codebase. It exposes a simple API that can be set up in minutes, powered by frameworks like PyTorch, Keras and Horovod. Finally, the web UI and callback utilities will make your training workflow more convenient than ever.

This section contains numerous examples of using BK.Synapse to help you get started. Select a lesson in your preferred framework on the navigation drawer to dive in.

## General Principle
BK.Synapse is built around 4 main concepts: datasets, data loaders, models, and jobs.

### Datasets
A dataset contains, well, data. A __BK.Synapse__ dataset is stored within a single folder, and can consist of arbitrary files (up to 10GB). _There is no required file format_. We don't make any assumptions about what type of data is required for your model. This is handled by data loaders, which are covered in the next section.

### Data Loaders
A data loader manages the connection between your datasets and the actual model. Think of it like PyTorch's `Dataset` or Keras' `Sequence` (in fact, they subclass those classes!). Data loaders makes up for the uncertainty of datasets and models. They're the glue layer that allows BK.Synapse to work with most data and model types.

### Models
Models contain the framework source code for your neural networks, and optional weight files. Like datasets, there is no required form of input other than what you define in your data loaders. However, there is a required interface that your models must adhere to. But you'll find that these methods can be trivially implemented and shouldn't affect you existing codebase.

### Jobs
Finally, jobs put everything together. They're basically parameters to your training script, and put your datasets, data loaders and models through a pipeline for training.
