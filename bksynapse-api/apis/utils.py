import os
import zipfile
import shutil


def unzip(zip_path, target_dir=None):
    if target_dir is None:
        target_dir = os.path.dirname(zip_path)
    
    zf = zipfile.ZipFile(zip_path, mode='r')
    zf.extractall(target_dir)
    zf.close()

def zip(zip_path, source_path):
    zip_name = zip_path.split('.')[-1]
    source_path = os.path.abspath(source_path)
    return shutil.make_archive(zip_name, zip, source_path)
