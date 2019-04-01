import os
import zipfile


def unzip(zip_path, target_dir=None):
    if target_dir is None:
        target_dir = os.path.dirname(zip_path)
    
    zf = zipfile.ZipFile(zip_path, mode='r')
    zf.extractall(target_dir)
    zf.close()


def generate_hostfile(nodes, path):
    
