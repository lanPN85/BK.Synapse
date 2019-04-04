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
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(source_path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

