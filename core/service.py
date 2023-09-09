from progress import ProgressBar
from requests import get
from pathlib import Path
from menu import Menu

def download(url: str, fileName: str, progressBar: ProgressBar, divider: int):
    with open(str(Path(__file__).parent.resolve().parent.resolve())+'/'+fileName, 'ab+') as f:
        download, i = get(url, stream=True), progressBar.percentage
        for chunk in download.iter_content(round(int(download.headers['Content-Length'])/divider)):
            f.write(chunk)
            progressBar.draw(i)
            i += 1