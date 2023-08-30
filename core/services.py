from requests import get

def download(url: str, path: str):
    with open(path, 'wb') as f:
        f.write(get(url).content)