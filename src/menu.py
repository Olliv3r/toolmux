from os import system

### Banner do toolmux

def banner():
    system('clear')
    banner = open('src/banner', 'r')
    print(f"{banner.read()}")
