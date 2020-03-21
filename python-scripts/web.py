import urllib.request
from pathlib import Path
import os

#
# Download 
#
def download_file_to_folder(url, folder):
    filename = url[url.rfind("/")+1:]
    data_folder = folder
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    target_path = os.path.join(data_folder, filename)
    print("Downloading %s to %s" % (url, target_path) )
    urllib.request.urlretrieve(url, target_path)
    return target_path
