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
from os import (system, mkdir, remove)


tools = Tools()
cmd = "Toolmux:~> "
dir = "/data/data/com.termux/files"

### Baixa a db se não existir
def downloading_db():
    print()
    print("\033[33;1mDownloading tool database...\033[0m")
    system("git clone https://github.com/Olliv3r/toolmux/ tmux > /dev/null 2>&1;mv tmux/banco.db .;rm tmux -rf")
    print("\033[33;1mDatabase downloaded successfully.\nRun the program again: '\033[32;2mpython toolmux.py\033[0m'")
    print()
    exit()

def menu_tools():
    global category

    banner()
    print(f"\tTotal of {tools.view_total_tools()} tools \n\tavailable")
    menu_tools_categories()

    category_option = input(cmd)

    if category_option == "1" or \
        category_option == "01":
        category = "information_collection"

    elif category_option == "2" or \
        category_option == "02":
        category = "vulnerability_analysis"

    elif category_option == "3" or \
        category_option == "03":
        category = "wireless_attacks"

    elif category_option == "4" or \
        category_option == "04":
        category = "web_applications"

    elif category_option == "5" or \
        category_option == "05":
        category = "sniffing_and_faking"

    elif category_option == "6" or \
        category_option == "06":
        category = "maintaining_access"

    elif category_option == "7" or \
        category_option == "07":
        category = "reporting_tools"

    elif category_option == "8" or \
        category_option == "08":
        category = "exploitation_tools"

    elif category_option == "9" or \
        category_option == "09":
        category = "forensic_tools"

    elif category_option == "10":
        category = "stress_test"

    elif category_option == "11":
        category = "password_attacks"

    elif category_option == "12":
        category = "reverse_engineering"

    elif category_option == "13":
        category = "hardware_hacking"
        
    elif category_option == "14":
        category = "extra"
    
    elif category_option == "0":
        exit("\nPrograma encerrado\n")

    else:
        menu_tools()
    
    view_tools(category)


### Mostra todas as ferramentas de acordo com a categoria

def view_tools(category):
    banner()
    print()
    
    query = f"SELECT * FROM {tools.tb_name} WHERE category = '{category}' ORDER BY name"
    result = tools.custom_selection(query)

    print(f"\t{category.replace('_', ' ').capitalize()}\n")
    count = 1
    for r in result:
        print(f"\t{count}) {r[1]}")
        count += 1
    
    print("\n\t0) Exit\n\tENTER) To go back\n")
    
    print()
    tool_option = input(cmd)

    if tool_option == "0":
        exit("\nProgram closed\n")

    if tool_option == "":
        menu_tools()

    tool_selected = find_index(result, int(tool_option) -1)

    if tool_selected[7] == "apt":
        apt_install_tool(tool_selected)

    elif tool_selected[7] == "apt not official":
        apt_not_official_install_tool(tool_selected)

    elif tool_selected[7] == "git":
        git_install_tool(tool_selected)

    elif tool_selected[7] == "wget":
        wget_install_tool(tool_selected)

        
    
### Descobre o índice da ferramenta

def find_index(data, option):
    tools_index = []

    for result in data:
        tools_index.append(data.index(result))

    if int(option) in tools_index:
        return data[int(option)]
    else:
        return False


### Instalação via APT official

def apt_install_tool(tool_selected):
    
    if tool_selected[5]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[5]} via {tool_selected[8]}...\033[0m")
        system(f"apt install {tool_selected[5]} -y")
        
    print(f"\033[33;1mInstalling {tool_selected[1]} via APT...\033[0m")
    system(f"apt install {tool_selected[2]} -y")
        
    verify_install_bin(tool_selected[2])
    back()


### Instalação via APT not official

def apt_not_official_install_tool(tool_selected):
    
    if tool_selected[5]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[5]} via APT...\033[0m")
        system(f"apt install {tool_selected[5]} -y")

    if exists(f"{dir}/usr/etc/apt/sources.list.d") == False:
        mkdir(f"{dir}/usr/etc/apt/sources.list.d")

    print(f"\033[33;1mAdding unofficial source {tool_selected[6]}...\033[0m")
    installer = split_url(tool_selected[6])
    system(f"wget {tool_selected[3]} -O {dir}/usr/etc/apt/sources.list.d/{installer}")
        
    print(f"\033[33;1mInstalling {tool_selected[1]} via APT not official...\033[0m")
    system(f"apt update && apt install {tool_selected[2]} -y")
    remove(f"{dir}/usr/etc/apt/sources.list.d/{installer}")
    verify_install_bin(tool_selected[2])
    back()

 
### Instalação via GIT

def git_install_tool(tool_selected):
    verify_and_remove(tool_selected[2])

    if tool_selected[5]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[5]} via APT...\033[0m")
        system(f"apt install {tool_selected[5]} -y")
    
    print(f"\033[33;1mInstalling {tool_selected[1]} via GIT...\033[0m")
    system(f"git clone {tool_selected[3]} {dir}/home/{tool_selected[2]}")
    verify_install_home(tool_selected[2])
    back()


    
### Instalação via wget

def wget_install_tool(tool_selected):
    if tool_selected[5]:
        print(f"\033[33;1mInstalling dependencies {tool_selected[5]} via APT...\033[0m")
        system(f"apt update && apt install {tool_selected[5]} -y")
        
    print(f"\033[33;1mInstalling {tool_selected[1]} via CURL...\033[0m")

    installer = split_url(tool_selected[3])
    
    system(f"wget {tool_selected[3]};bash ./{installer}")
    
    if isfile(f"./{installer}") == True:
        remove(f"./{installer}")
    
    verify_install_bin(tool_selected[2])
    back()

    
### Retorna o nome do instalador da url
    
def split_url(url):
    r_url = url.split("/")
    return r_url[-1]


### Verifica instalação via APT ou APT not offical:

def verify_install_bin(file):
    print()
    if isfile(f"{dir}/usr/bin/{file}") == True:
        print(f"\033[32;1m{file} installed\033[0m")
    else:
        print(f"\033[31;1m{file} not installed\033[0m")


### Verifica instalação via GIT

def verify_install_home(directory):
    print()
    if isdir(f"{dir}/home/{directory}") == True:
        print(f"\033[32;1m{directory} installed\033[0m")
    else:
        print(f"\033[31;1m{directory} not installed\033[0m")


### Verifica se existe o projeto antigo e o remove

def verify_and_remove(directory):
    if isdir(f"{dir}/home/{directory}") == True:
        print(f"\033[34;1m{directory} found. downloading new {directory}...\033[0m")
        system(f"rm -rf {dir}/home/{directory}")
    print()

### Voltar uma tela para trás ou sair

def back():
    print("\n 0) Exit \n ENTER) To go back\n")
    
    option = input(cmd)

    if option == "0":
        exit("\nProgram closed\n")
    else:
        view_tools(category)

if not tools.custom_selection():
    downloading_db()

menu_tools()
