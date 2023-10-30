#!/usr/bin/env python
# Instalador de ferramentas
#
# By Oliver Silva
#
#

from src.banco import *
from src.menu import *
from time import sleep
from os.path import (isfile, isdir ,exists)
from os import (system, mkdir, remove, getlogin)
try:
    import requests
except ModuleNotFoundError as err:
    exit(err)

tool = Tool()
__version__ = "0.0.4"

cmd = "toolmux"
dir = "/data/data/com.termux/files"

### Checa acesso a internet:
def check_internet():
    print("Checking internet...")
    try:
        requests.request('get', 'https://www.google.com', timeout=5)
        return True
    except request.exceptions.ConnectionError:
        return False

### Baixa a base de ferramentas se não existir:
def downloading_db():
    if check_internet() == False:
        exit("Internet is not connected")
    print("Internet is connected")

    print()
    print("\033[33;1mDownloading tool database...\033[0m")
    system("curl -LO -s https://raw.githubusercontent.com/Olliv3r/App/main/app.db;sleep 1")
    exit("\033[33;1mDatabase downloaded successfully.\nRun the program again: '\033[32;2m./toolmux.py\033[0m'")

### Menu se categorias:
def menu_tools():
    global category

    banner()
    print(f"\tVersion: {__version__}\n\n\tTotal of {total} tools \n\tavailable\n")
    menu_tools_categories()

    category_option = input(f"{cmd}-> ")

    if category_option == "1" or \
        category_option == "01":
        category = "Information Collection"

    elif category_option == "2" or \
        category_option == "02":
        category = "Vulnerability Analysis"

    elif category_option == "3" or \
        category_option == "03":
        category = "Wireless Attacks"

    elif category_option == "4" or \
        category_option == "04":
        category = "Web Applications"

    elif category_option == "5" or \
        category_option == "05":
        category = "Sniffing and Faking"

    elif category_option == "6" or \
        category_option == "06":
        category = "Maintaining Access"

    elif category_option == "7" or \
        category_option == "07":
        category = "Reporting Tools"

    elif category_option == "8" or \
        category_option == "08":
        category = "Exploitation Tools"

    elif category_option == "9" or \
        category_option == "09":
        category = "Forensic Tools"

    elif category_option == "10":
        category = "Stress Test"

    elif category_option == "11":
        category = "Password Attacks"

    elif category_option == "12":
        category = "Reverse Engineering"

    elif category_option == "13":
        category = "Hardware Hacking"
        
    elif category_option == "14":
        category = "Extra"
    
    elif category_option == "0" or \
        category_option == "00":
        exit("\nPrograma encerrado\n")

    else:
        menu_tools()
    
    view_tools(category)


### Mostra todas as ferramentas de acordo com a categoria:
def view_tools(category):
    banner()
    print()
    
    query = f"SELECT * FROM {tool.tb_name} WHERE category = '{category}' ORDER BY name"
    result = tool.instrunction(query).fetchall()

    print(f"\t{category}\n")

    for index, r in enumerate(result):
        print(f"\t{index +1}) {r[1]}")
    
    print("\n\t0) Exit\n\tENTER) To go back\n")
    
    print()
    tool_option = input(f"{cmd}-> ")

    if tool_option == "0":
        exit("\nProgram closed\n")

    if tool_option == "":
        menu_tools()

    options = tool_option.split(",")

    for option in options:
        try:
            tool_selected = find_index(option, result)

            if tool_selected[7] == "apt":
                apt_install_tool(tool_selected)

            elif tool_selected[7] == "apt not official":
                apt_not_official_install_tool(tool_selected)
            elif tool_selected[7] == "git":
                git_install_tool(tool_selected)

            elif tool_selected[7] == "curl":
                curl_install_tool(tool_selected)
        except TypeError as err:
            print(f"\n\033[1;33mIndex {option} does not exist in the list of tools above!\033[0m")

    back()
         
### Retorna o item do indice escolhido:
def find_index(option, result):
    indexes = []

    for r in result:
        indexes.append(result.index(r))

    if (int(option) -1) in indexes:
        return result[int(option) -1]
    else:
        return False

### Instalação via APT official:
def apt_install_tool(tool_selected):
    
    if tool_selected[9]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[9]} via APT...\033[0m")
        system(f"apt update && apt install {tool_selected[9]} -y")

    print(f"\033[33;1mInstalling {tool_selected[1]} via APT...\033[0m")
    system(f"apt install {tool_selected[3]} -y")
        
    verify_install_bin(tool_selected[3], tool_selected[1])

### Instalação via APT not official:
def apt_not_official_install_tool(tool_selected):
    
    if tool_selected[8]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[9]} via APT...\033[0m")
        system(f"apt install {tool_selected[9]} -y")

    if exists(f"{dir}/usr/etc/apt/sources.list.d") == False:
        mkdir(f"{dir}/usr/etc/apt/sources.list.d")

    print(f"\033[33;1mAdding unofficial source {tool_selected[2]}...\033[0m")
    installer = split_url(tool_selected[6])
    system(f"curl -L -s {tool_selected[6]} -o {dir}/usr/etc/apt/sources.list.d/{installer}")
        
    print(f"\033[33;1mInstalling {tool_selected[1]} via APT not official...\033[0m")
    system(f"apt update && apt install {tool_selected[3]} -y")
    remove(f"{dir}/usr/etc/apt/sources.list.d/{installer}")
    verify_install_bin(tool_selected[4], tool_selected[1])

### Instalação via GIT:
def git_install_tool(tool_selected):
    verify_and_remove(tool_selected[3])

    if tool_selected[9]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[9]} via APT...\033[0m")
        system(f"apt install {tool_selected[9]} -y")
    
    print(f"\033[33;1mInstalling {tool_selected[1]} via GIT...\033[0m")
    system(f"git clone {tool_selected[6]} {dir}/home/{tool_selected[3]}")
    verify_install_home(tool_selected[3], tool_selected[1])
 
### Instalação via curl:
def curl_install_tool(tool_selected):
    if tool_selected[9]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[9]} via APT...\033[0m")
        system(f"apt update && apt install {tool_selected[9]} -y")
        
    print(f"\033[33;1mInstalling {tool_selected[1]} via CURL...\033[0m")

    installer = split_url(tool_selected[6])
    
    system(f"curl -LO {tool_selected[6]};bash {installer}")
    
    if isfile(f"{installer}") == True:
        remove(f"{installer}")

    verify_install_bin(tool_selected[4], tool_selected[1])
    
### Retorna o nome do instalador da url:
def split_url(url):
    r_url = url.split("/")
    return r_url[-1]

### Verifica instalação via APT, APT not offical e CURL:
def verify_install_bin(custom_alias, name):
    print()

    if isfile(f"{dir}/usr/bin/{custom_alias}") == True:
        print(f"\033[32;1m{name} installed\033[0m")
    else:
        print(f"\033[31;1m{name} not installed\033[0m")

### Verifica instalação via GIT:
def verify_install_home(directory, name):
    print()
    if isdir(f"{dir}/home/{directory}") == True:
        print(f"\033[32;1m{name} installed\033[0m")
    else:
        print(f"\033[31;1m{name} not installed\033[0m")


### Verifica a existência do projeto antigo e o remove:
def verify_and_remove(directory):
    if isdir(f"{dir}/home/{directory}") == True:
        print(f"\033[34;1m{directory} found. downloading new {directory}...\033[0m")
        system(f"rm -rf {dir}/home/{directory}")
    print()

### Voltar uma tela para trás ou sair:
def back():
    print("\n 0) Exit \n ENTER) To go back\n")
    
    option = input(f"{cmd}-> ")

    if option == "0":
        exit("\nProgram closed\n")
    else:
        view_tools(category)

### Messagem apôs o encerramento do programa
def warnning():
    system("stty -echoctl")
    print("\n\033[31;1mProgram interrupt\033[0m\n")


### Função principal
def main():
    global total

    if isfile('app.db'):

        result = tool.get_total_tool()

        if result == False:
            downloading_db()
        
        total = result.fetchall()[0][0]
        menu_tools()

    else:
        downloading_db()


if __name__ == "__main__":
    main()
