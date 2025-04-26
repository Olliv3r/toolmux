#!/usr/bin/env python3
# Tool Installer For Termux - By Oliver Silva
#

# Importação de módulosa
import shutil
import os
import sys
import time
from os.path import isfile, isdir

from core import TOOL, VERSION, TOTAL_TOOLS, AUTHOR
from db import DB_PATH
from banner import load_banner

try:
    import requests
    from requests.exceptions import ConnectionError
except ModuleNotFoundError as err:
    sys.exit("\033[33;1m[!] O módulo 'requests' é necessário. Instale com: pip install requests \033[0m")

PROMPT = f"\033[1;34mToolmux\033[0m > "
TERMUX_DIR = "/data/data/com.termux/files"

### Verifica se roda no termux
def check_termux_os():
    return os.path.exists(TERMUX_DIR)

### Verifica conexão com a internet
def check_internet():
    try:
        requests.get('https://www.google.com', timeout=5)
        return True
    except ConnectionError:
        return False
 
### Faz download da base de ferramentas
def downloading_db():
    if not check_internet():
        sys.exit("\033[31;1m[×] A Internet não está conectada\033[0m")
        
    print("\033[34;1m[*] Baixando banco de dados de ferramentas...\033[0m")

    url_db = 'https://github.com/Olliv3r/Toolmux-DB/raw/refs/heads/main/toolmux.db'
    response = requests.get(url_db)

    if response.status_code == 200:
        with open(DB_PATH, 'wb') as f:
            f.write(response.content)

        sys.exit("\033[32;1m[√] Banco de dados baixado com sucesso.\n\033[33;1m[?] Execute novamente com 'python3 toolmux.py'\033[0m")
        time.sleep(0.25)
    
    else:
        sys.exit('\033[31;1m[×] Falha ao baixar a base de ferramentas\033[0m')

### Cardápio de opçôes
def menu_options():
    os.system('clear')
    print(load_banner())
    
    print(f"\tv{VERSION}\n\033[1;32m\n+ -- -- +=[ Author: {AUTHOR} | Homepage: http://toolmux.rf.gd\n+ -- -- +=[ {TOTAL_TOOLS} Tools\033[0m")
    print("\n\n1) View Categories\n2) Report Bugs\n3) Help\nq) Exit\n")

    options_input = {
        '1': menu_categories,
        '2': report_bugs,
        '3': helper,
        'q': warning
    }

    try:
        choice = input(f"\n{PROMPT}")
        
    except(EOFError, KeyboardInterrupt):
        return warning()

    options_input.get(choice, menu_options)()
    
# Centraliza texto dinamicamente
def print_centered(text, filchar=" "):
    text = f" {text} "
    
    try:
        terminal_size = os.get_terminal_size().columns
    except OSError:
        terminal_size = 80

    print(f"\n{text.center(terminal_size, filchar)}\n")


def split_into_columns(data, num_columns):
    columns = [[] for _ in range(num_columns)]
    for i, item in enumerate(data):
        columns[i % num_columns].append(item)
    return columns

# Divide categorias e ferramentas em até 4 colunas
def display_group(result=None, terminal_width=None):
    if not result:
         print_centered("Nenhuma categoria ou ferramenta encontrada.")
         return []
         
    display_list = [f"{i+1}) {row[1]}" for i, row in enumerate(result)]

    if display_list: 
        max_length = len(max(display_list, key=len))
    else:
        max_length = 0
    
    ids = [row[0] for row in result]

    if terminal_width < 60:
        columns_count = 1
    elif terminal_width < 90:
        columns_count = 2
    elif terminal_width < 130:
        columns_count = 3
    else:
        columns_count = 4

    columns = split_into_columns(display_list, columns_count)

    max_len = max(len(item) for item in display_list)
    max_rows  = max(len(col) for col in columns)

    for i in range(max_rows):
        row = [
            columns[j][i] if i < len(columns[j]) else "" for j in range(columns_count)
        ]
        print("\t".join(item.ljust(max_length) for item in row))
    return ids

### Lista de categorias
def menu_categories():
    os.system('clear')
    print(load_banner())
    
    result = TOOL.sq('SELECT * FROM category ORDER BY id', ()).fetchall()

    print_centered("Todas as categorias", "*")

    terminal_width = shutil.get_terminal_size((80, 20)).columns
    ids = display_group(result, terminal_width)
        
    print("\nSelecione uma categoria ou pressione [Enter] para retornar, ou [q] para encerrar.")

    category_count = f"{TOOL.sq('select count(*) from category', ()).fetchone()[0]}"

    try:
        category_option = input(f"\n{PROMPT}")

        if category_option == "":
            menu_options()
             
        elif category_option == "q":
            warning()

        elif category_option.isdigit() and 1 <= int(category_option) <= len(ids):
            category_id = ids[int(category_option) -1]
            view_tools(category_option)
            
        else:
            text_error = f"\n\033[1;31mTente valores entre 1 e {category_count}.\033[0m"
            menu_back(menu_name="menu_categorias", alert=text_error)
            
    except Exception as e:
        text_error = f"\n\033[1;31m{e}! Tente valores entre 1 e {category_count}.\033[0m"
        return menu_back(menu_name="menu_categorias", alert=text_error)
        
    except(EOFError, KeyboardInterrupt):
        return warning()
        
### Mostra todas as ferramentas de acordo com a categoria
def view_tools(category_id):
    os.system('clear')
    print(load_banner())
    
    result = TOOL.sq(f"SELECT * FROM {TOOL.tb_name} WHERE category_tool_id = ? ORDER BY name", (category_id,)).fetchall()
    
    print_centered("Todas as Ferramentas", "*")
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    display_group(result, terminal_width)

    print("\nSelecione uma ferramenta ou pressione [Enter] para retornar, ou [q] para encerrar.")
    print()
    
    try:
        tool_option = input(f"{PROMPT}")
 
        if tool_option == "q":
            warning()
            
        elif tool_option == "":
            menu_categories()
            return

        options = tool_option.split(",")

        for option in options:
            tool_selected = find_index(option, result)
                
            if tool_selected[8] == 1:
                apt_install_tool(tool_selected, category_id=category_id)
                
            elif tool_selected[8] == 2:
                git_install_tool(tool_selected, category_id=category_id)

        menu_back(menu_name="menu_ferramentas", category_id=category_id)
            
    except Exception as e:
        text_error = f"\n\033[1;31m{e}! Tente valores entre 1 e {len(result)}.\033[0m"
        menu_back(menu_name="menu_ferramentas", category_id=category_id, alert=text_error)

    except(EOFError, KeyboardInterrupt):
        warning()
         
### Retorna o item do indice selecionado
def find_index(option, result): 
    try:
        option = int(option)

        if 1 <= option <= len(result):
            return result[option -1]
        else:
            return False
            
    except (ValueError, TypeError):
        pass
    return False

### Instalação via APT official
def apt_install_tool(tool_selected, category_id):
    if tool_selected[6]:
        print(f"\033[33;1mInstalando dependências {tool_selected[1]} com APT...\033[0m")
        os.system(f"apt update && apt install {tool_selected[2]} -y")

    print(f"\033[33;1mInstalando {tool_selected[1]} com APT...\033[0m")
    os.system(f"apt install {tool_selected[2]} -y")        
    verify_install_bin(tool_selected[2], tool_selected[1], category_id)

### Instalação via GIT
def git_install_tool(tool_selected, category_id = None):
    verify_and_remove(tool_selected[4])

    if tool_selected[6]:
        print(f"\033[33;1mInstalando dependências {tool_selected[1]} via APT...\033[0m")
        os.system(f"apt install {tool_selected[6]} -y")
    
    print(f"\033[33;1mInstalando {tool_selected[1]} com GIT...\033[0m")
    os.system(f"git clone {tool_selected[5]} {TERMUX_DIR}/home/{tool_selected[4]}")

    installation_tip = TOOL.sq('SELECT installation_tip FROM tool WHERE id=?', (str(tool_selected[0]))).fetchone()

    verify_install_home(tool_selected[4], tool_selected[1], installation_tip, category_id)

### Verifica instalação via APT, APT not offical e CURL
def verify_install_bin(alias, name, category_id):
    print()

    if os.path.isfile(f"{TERMUX_DIR}/usr/bin/{alias}") == True:
        print(f"\033[32;1m{name} instalado\033[0m")
    else:
        print(f"\033[31;1m{name} não instalado\033[0m")

### Verifica instalação via GIT
def verify_install_home(directory, name, tip, category_id):
    print()

    if os.path.isdir(f"{TERMUX_DIR}/home/{directory}") == True:
        print(f"\033[32;1m{name} instalado\033[0m")

        if tip[0] != "":
            print('\n\033[1;33mDica de instalação!\033[0m\n\nPara continuar com a instalação copie e cole este comando em uma nova aba:\033[0m\n\n')
            print(f"\033[3;33m{tip[0]}\033[0m\n")
        
    else:
        print(f"\033[31;1m{name} não instalado\033[0m")


### Verifica a existência do projeto antigo e o remove
def verify_and_remove(directory):
    if os.path.isdir(f"{TERMUX_DIR}/home/{directory}") == True:
        print(f"\033[34;1m{directory} encontrado. baixando novo {directory}...\033[0m")
        os.system(f"rm -rf {TERMUX_DIR}/home/{directory}")

    print()

# NAVEGA ATÉ UM MENU
def back_to(menu_name=None, category_id=None):
    
    menu_actions = {
        'menu_opcoes': menu_options,
        'menu_categorias': menu_categories,
        'menu_ferramentas': lambda: view_tools(category_id),
        'menu_back': menu_back
    }

    action = menu_actions.get(menu_name)

    if action:
        return action()


# Menu que auxilia o usuário após a instalação de uma ferramenta
def menu_back(menu_name=None, category_id=None, alert=None):
    if alert:
        print(alert)

    print("\nPressione [Enter] para retornar ou [m] para ir ao menu principal, ou [q] para encerrar.\n")
    
    try:
        option = input(f'{PROMPT}')
        
        if option == "":
            if menu_name == "menu_categorias":
                return back_to(menu_name="menu_categorias")

            elif menu_name == "menu_ferramentas":
                return back_to(menu_name="menu_ferramentas", category_id=category_id)

        option_actions = {
            'm': menu_options,
            'q': warning
        }

        action = option_actions.get(option)

        if action:
            return action()
            
        else:
            print(f'\033[1;31mInvalid input!\033[0m')
            menu_back(menu_name="menu_ferramentas", category_id=category_id)
            
    except Exception as e:
        print(f'\033[1;31m{e}\033[0m')
        return back_to(menu_name="menu_back", category_id=category_id)

    except (KeyboardInterrupt, EOFError):
        return warning()

### Mensagem apôs o encerramento do programa
def warning():
    sys.exit("\n\033[1;31mPrograma interrompido\033[0m\n")

def report_bugs():
    print("Report Bug")

def helper():
    print("Helper")

### Função Principal
def main():
    if not check_termux_os():
        sys.exit("\033[31;1m[×] Termux OS não foi detectado\033[0m")
    
    print("\033[32;1m[√] Termux OS detectado\033[0m")
    time.sleep(0.25)

    if TOTAL_TOOLS > 0:
        menu_options()
    else:
        downloading_db()

if __name__ == "__main__":
    main()
