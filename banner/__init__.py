import os

def load_banner():
    path = os.path.join(os.path.dirname(__file__), 'banner.txt')

    with open(path, encoding="utf-8") as f:
        return f.read()
