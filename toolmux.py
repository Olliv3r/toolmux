#!/usr/bin/env python3
# Tool Installer For Termux - By Oliver Silva
#

# Importação de módulosa
import shutil
import os
import sys
import time
from os.path import isfile, isdir
from colorama import Fore, Style, init

from core import total_tools, VERSION, AUTHOR, BANNER_MENU, BANNER_REPORT, session
from core.report_bug import send_report_bug
from core.models import Category, Tool, tool_category
import sqlalchemy as sa

init(autoreset=True)

PROMPT = f"\033[1;34mToolmux\033[0m > "
TERMUX_DIR = "/data/data/com.termux/files"

### Verifica se roda no termux  
def check_termux_os():
    return os.path.exists(TERMUX_DIR)

### Cardápio de opçôes
def menu_options():
    os.system('clear')
    print(BANNER_MENU)

    print(f"\t{Fore.GREEN}v{VERSION}\n\n{Fore.WHITE}+ -- -- +=[ Author: {AUTHOR} | Homepage: https://toolmuxapp.pythonanywhere.com\n+ -- -- +=[ {total_tools} Tools{Style.RESET_ALL}")
    print(f"\n\n{Fore.CYAN}1) {Fore.WHITE}View Categories\n{Fore.CYAN}2) {Fore.WHITE}Report Bugs\n{Fore.CYAN}3) {Fore.WHITE}Help\n{Fore.CYAN}q) {Fore.WHITE}Exit{Style.RESET_ALL}\n")

    options_input = {
        '1': menu_categories,
        '2': menu_report,
        '3': helper,
        'q': warning
    }

    try:
        choice = input(f"\n{PROMPT}")

    except(EOFError, KeyboardInterrupt):
        return warning()


    try:
        action = options_input.get(choice)()

    except TypeError:
        print_status("\nOpção inválida...aguarde\n", "red")
        time.sleep(1)
        menu_options()
        
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
         
    display_list = [f"{Fore.CYAN}{i+1}) {Fore.WHITE}{row.name}" for i, row in enumerate(result)]

    if display_list: 
        max_length = len(max(display_list, key=len))
    else:
        max_length = 0
    
    ids = [row.id for row in result]

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
    print(BANNER_MENU)
    
    categories = session.scalars(sa.select(Category).order_by(Category.id)).all()
    total_categories = session.scalar(sa.select(sa.func.count(Category.id)))

    print_centered("Todas as categorias", "*")

    terminal_width = shutil.get_terminal_size((80, 20)).columns
    ids = display_group(categories, terminal_width)
        
    print("\nSelecione uma categoria ou pressione [Enter] para retornar, ou [q] para encerrar.")

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
            text_error = f"\n\033[1;31mTente valores entre 1 e {total_categories}.\033[0m"
            menu_back(menu_name="menu_categorias!l", alert=text_error)
            
    except Exception as e:
        text_error = f"\n\033[1;31m{e}! Tente valores entre 1 e {total_tools}.\033[0m"
        return menu_back(menu_name="menu_categorias", alert=text_error)
        
    except(EOFError, KeyboardInterrupt):
        return warning()
        
### Mostra todas as ferramentas de acordo com as categorias

def view_tools(category_id):
    os.system('clear')
    print(BANNER_MENU)

    tools = session.scalars(
        sa.select(Tool).join(tool_category, Tool.id == tool_category.c.tool_id).filter(tool_category.c.category_id == category_id)
    ).all()

    total_tools_filter = session.scalar(
        sa.select(sa.func.count(Tool.id)).join(tool_category, Tool.id == tool_category.c.tool_id).filter(tool_category.c.category_id == category_id)
    )

    print_centered("Todas as Ferramentas", "*")
    terminal_width = shutil.get_terminal_size((80, 20)).columns
    display_group(tools, terminal_width)

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
            tool_selected = find_index(option, tools)

            if tool_selected.installation_type_id == 1:
                apt_install_tool(tool_selected, category_id=category_id)
                
            elif tool_selected.installation_type_id == 2:
                git_install_tool(tool_selected, category_id=category_id)

        menu_back(menu_name="menu_ferramentas", category_id=category_id)
            
    except Exception as e:
        text_error = f"\n\033[1;31m{e}! Tente valores entre 1 e {(total_tools_filter)}.\033[0m"
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

def print_status(message, color="white"):
    colors = {
        "white": "\033[0m",
        "yellow": "\033[1;33m",
        "green": "\033[1;32m",
        "red": "\033[1;31m",
        "magenta": "\033[1;35m",
        "cyan": "\033[1;36m",
        "blue": "\033[1;34m"
    }
    print(f'{colors.get(color, colors["white"])}{message}{colors["white"]}')

### Instalação via APT official
def apt_install_tool(tool_selected, category_id):
    tool_name = tool_selected.name
    package_name = tool_selected.alias
    has_dependencies = tool_selected.dependencies

    if has_dependencies:
        print_status(f"Instalando dependências para {tool_name}...", "green")
        os.system(f"apt update && apt install {package_name} -y")

    print_status(f"Instalando {tool_name} com APT...", "green")
    install_result = os.system(f"apt install {package_name} -y")

    if install_result == 0:
        print_status(f"\n✅ {tool_name} instalado com sucesso!", "green")
    else:
        print_status(f"\n❌ {tool_name} não foi instalado corretamente", "red")

### Instalação via GIT
def git_install_tool(tool_selected, category_id = None):
    directory_name = tool_selected.name_repo
    tool_name = tool_selected.name
    has_dependencies = tool_selected.dependencies
    package_name = tool_selected.alias
    tool_id = tool_selected.id
    tool_link = tool_selected.link
    
    verify_and_remove(directory_name)

    if has_dependencies:
        print_status(f"Instalando dependências para {tool_name}...", "green")
        os.system(f"apt install {has_dependencies} -y")
        
    print_status(f"Instalando {tool_name} com GIT...", "green")
    os.system(f"git clone {tool_link} {TERMUX_DIR}/home/{directory_name}")

    installation_tip = session.scalar(
        sa.select(Tool.installation_tip).filter(Tool.id == tool_id)
    )

    verify_install_home(directory_name, tool_name, installation_tip, category_id)


### Verifica instalação via GIT
def verify_install_home(directory, name, installation_tip, category_id):
    print()

    project_path = f"{TERMUX_DIR}/home/{directory}"

    if os.path.isdir(project_path):
        print_status(f"✅ A instalação do {name} foi concluída com sucesso!\n", "green")

        if installation_tip != "":
            print_status("Agora, siga a dica abaixo para finalizar a configuração:\n", "blue")
            print_status("Copie e cole o seguinte comando em uma nova aba do Termux:\n", "blue")
            print("\033[93m-\033[0m"*len(installation_tip))
            print_status(installation_tip, "green")
            print("\033[93m-\033[0m"*len(installation_tip))

            print_status(f"\nDepois de executar o comando acima, seu {name} estará pronto para uso!", "blue")
        else:
            print_status(f"Nenhuma dica adicional fornecida para {name}.")
    else:
        print_status(f"❌ {name} não foi instalado corretamente.", "red")


### Verifica a existência do projeto antigo e o remove
def verify_and_remove(directory):
    project_path = f"{TERMUX_DIR}/home/{directory}"
    
    if os.path.isdir(project_path):
        print_status(f"{directory} encontrado. baixando novo {directory}...", "blue")
        os.system(f"rm -rf {project_path}")

    print()

# NAVEGA ATÉ UM MENU
def back_to(menu_name=None, category_id=None):
    
    menu_actions = {
        'menu_opcoes': menu_options,
        'menu_categorias': menu_categories,
        'menu_ferramentas': lambda: view_tools(category_id),
        'menu_report': menu_report,
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

            elif menu_name == "menu_report":
                return back_to(menu_name="menu_report")


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

def menu_report():
    os.system('clear')
    print(BANNER_REPORT)
    
    print_centered("Relatório de Bug - Toolmux")
    description = input("Descreva o problema encontrado:\n >").strip()
    screenshot = input("Se tiver uma captura de tela. Informe o caminho do arquivo (ou deixe vazio para pular):\n>").strip()
    user_name = input('Seu nome (ou deixe vazio para pular):\n>').strip()

    send_report_bug(description, user_name, screenshot)

    menu_back(menu_name="menu_report")

def helper():
    print("Helper")

### Função Principal
def main():
    if not check_termux_os():
        sys.exit("\033[31;1m[×] Termux OS não foi detectado\033[0m")
    
    print("\033[32;1m[√] Termux OS detectado\033[0m")
    time.sleep(0.05)

    menu_options()

if __name__ == "__main__":
    main()
