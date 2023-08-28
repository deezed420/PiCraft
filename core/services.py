from progress import ProgressBar
from requests import get
from menu import Menu

def download(url: str, path: str):
    with open(url, 'wb') as f:
        f.write(get(url).content)