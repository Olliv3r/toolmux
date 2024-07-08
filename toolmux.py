#!/usr/bin/env python
# Instalador de ferramentas somente no emulador termux
#
# By Oliver Silva
#
#

from src.banco import *
from src.menu import banner
from time import sleep
from os.path import (isfile, isdir ,exists)
from os import (system, mkdir, remove, getlogin, environ)
try:
    from requests import request
    from requests.exceptions import ConnectionError
except ModuleNotFoundError as err:
    exit(err)

tool = Tool()
__version__ = "0.0.7"

cmd = f"\033[1;34mToolmux\033[0m > "
dir = "/data/data/com.termux/files"


### Verifica se roda no termux
def check_termux_os():
    if environ.get("TERMUX_APP__PACKAGE_NAME") is not None:
        return True
    else:
        return False

### Verifica o acesso a internet
def check_internet():
  try:
    request('get', 'https://www.google.com', timeout=5)
    return True
  except ConnectionError:
    return False
 
### Faz download da base de ferramentas
def downloading_db():
  if check_internet() == False:
    exit("Internet is not connected")
  print("Internet is connected")
  print()
  print("\033[33;1mDownloading tool database...\033[0m")
  system("curl -LO -s https://raw.githubusercontent.com/Olliv3r/Toolmux-Web/main/toolmux.db;sleep 1")
  exit("\033[33;1mDatabase downloaded successfully.\nRun the program again: '\033[32;2m./toolmux.py\033[0m'")

### Cardápio de opçôes
def menu_options():
  banner()
  print(f"\tv{__version__}\n\033[1;32m\n+ -- -- +=[ Author: Olliv3r | Homepage: http://toolmux.rf.gd\n+ -- -- +=[ {total} Tools\033[0m")
  print("\n\n1) View Categories\n2) Report Bugs\n3) Help\n0) Exit\n")

  try:
    menu_option = input(f"\n{cmd}")
  except EOFError:
    warning()
  except KeyboardInterrupt:
    warning()

  if menu_option == "":
    menu_options()

  elif menu_option == "1" or menu_option == "01":
    menu_categories()
    
  elif menu_option == "2" or menu_option == "02":
    report_bugs()
    
  elif menu_option == "3" or menu_option == "03":
    helper()

  elif menu_option == "0" or menu_option == "00":
    warning()
    
  else:
    menu_options()

### Cardápio de categorias
def menu_categories():
  global category
  global category_id
  
  ids = []
  result = tool.sq('SELECT * FROM category ORDER BY id').fetchall()

  print()
  print("*"*27+" All Categories "+"*"*27)
  print()

  group_category1 = []
  group_category2 = []
  
  for row in result:
    if row[0] <= len(result) / 2:
      group_category1.append(f"{row[0]}) {row[1]}")

    if row[0] > len(result) / 2:
      group_category2.append(f"{row[0]}) {row[1]}")
    ids.append(row[0])

  if group_category1 and group_category2:
    max_length = max(len(max(group_category1, key = len)), len(max(group_category2, key = len)))
  elif group_category1:
    max_length = len(max(group_category1, key = len))
  elif group_category2:
    max_length = len(max(group_category2, key = len))
  else:
    max_length = 0

  for i in range(max(len(group_category1), len(group_category2))):
    option1 = group_category1[i] if i < len(group_category1) else ""
    option2 = group_category2[i] if i < len(group_category2) else ""
    print(f"{option1.ljust(max_length)}\t\t\t{option2}")
  print("\nSelect a category or press (enter) to back or (0) to exit.")
  
  try:
    category_option = input(f"\n{cmd}")
  except EOFError:
    warning()
  except KeyboardInterrupt:
    warning()

  if category_option == "":
    menu_options()
  elif int(category_option) in ids:
    category = result[int(category_option) -1][1]
    category_id = category_option
    view_tools(category, category_id)
  elif category_option == "0" or\
    category_option == "00":
    warning()
  else:
    sleep(0.2)
    menu_categories()
 
### Mostra todas as ferramentas de acordo com a categoria
def view_tools(category, category_id):
  result = tool.sq(f"SELECT * FROM {tool.tb_name} WHERE category_tool_id = '{category_id}' ORDER BY name").fetchall()
  
  print()
  print("*"*27+" All Tools "+"*"*27)
  print()

  group_tools1 = []
  group_tools2 = []

  for index, row in enumerate(result):
    if row[0] <= len(result) / 2:
      group_tools1.append(f"{index +1}) {row[1]}")
          
    if row[0] > len(result) / 2:
      group_tools2.append(f"{index +1}) {row[1]}")

  max_length_group1 = len(max(group_tools1, key=len)) if group_tools1 else 0
  max_length_group2 = len(max(group_tools2, key=len)) if group_tools2 else 0
      
  max_length = max(max_length_group1, max_length_group2)

  for i in range(max(len(group_tools1), len(group_tools2))):
    option1 = group_tools1[i] if i < len(group_tools1) else ""
    option2 = group_tools2[i] if i < len(group_tools2) else ""

    print(f"{option1.ljust(max_length)}\t\t\t{option2}")
  print("\nSelect a tool or press (enter) to back or (0) to exit.")
  print()

  try:
    tool_option = input(f"{cmd}")
  except EOFError:
    warning()
  except KeyboardInterrupt:
    warning()
 
  if tool_option == "0":
    warning()
  elif tool_option == "":
    menu_categories()

  options = tool_option.split(",")

  for option in options:
    try:
      tool_selected = find_index(option, result)
    
      if tool_selected[8] == 1:
        apt_install_tool(tool_selected)
      elif tool_selected[8] == 2:
        git_install_tool(tool_selected)
    
    except TypeError as err:
      print(f"\n\033[1;33mIndex {option} does not exist in the list of tools above!\033[0m")
  back()
         
### Retorna o item do indice selecionado
def find_index(option, result):
  indexes = []

  for r in result:
    indexes.append(result.index(r))

  if (int(option) -1) in indexes:
    return result[int(option) -1]
  else:
    return False

### Instalação via APT official
def apt_install_tool(tool_selected):
  if tool_selected[6]:
    print(f"\033[33;1mInstalling dependencies {tool_selected[1]} via APT...\033[0m")
    system(f"apt update && apt install {tool_selected[2]} -y")

  print(f"\033[33;1mInstalling {tool_selected[1]} via APT...\033[0m")
  system(f"apt install {tool_selected[2]} -y")        
  verify_install_bin(tool_selected[2], tool_selected[1])

### Instalação via GIT
def git_install_tool(tool_selected):
  verify_and_remove(tool_selected[4])

  if tool_selected[6]:
    print(f"\033[33;1mInstalling dependencies {tool_selected[1]} via APT...\033[0m")
    system(f"apt install {tool_selected[6]} -y")
    
  print(f"\033[33;1mInstalling {tool_selected[1]} via GIT...\033[0m")
  system(f"git clone {tool_selected[5]} {dir}/home/{tool_selected[4]}")

  installation_tip = tool.sq(f'SELECT installation_tip FROM tool WHERE id={tool_selected[0]}').fetchone()

  verify_install_home(tool_selected[4], tool_selected[1], installation_tip)

### Verifica instalação via APT, APT not offical e CURL
def verify_install_bin(alias, name):
  print()

  if isfile(f"{dir}/usr/bin/{alias}") == True:
    print(f"\033[32;1m{name} installed\033[0m")
  else:
    print(f"\033[31;1m{name} not installed\033[0m")

### Verifica instalação via GIT
def verify_install_home(directory, name, tip):
  print()
  if isdir(f"{dir}/home/{directory}") == True:
    print(f"\033[32;1m{name} installed\033[0m")

    if tip[0] != "":
      print('\n\033[1;33mDica de instalação!\033[0m\n\nPara continuar com a instalação copie e cole este comando em uma nova aba:\033[0m\n\n')
      print(f"\033[3;33m{tip[0]}\033[0m\n")
  else:
    print(f"\033[31;1m{name} not installed\033[0m")


### Verifica a existência do projeto antigo e o remove
def verify_and_remove(directory):
  if isdir(f"{dir}/home/{directory}") == True:
    print(f"\033[34;1m{directory} found. downloading new {directory}...\033[0m")
    system(f"rm -rf {dir}/home/{directory}")
  print()

### Voltar uma tela para trás ou sair
def back():
  print("\n 0) Exit \n ENTER) To go back\n")
   
  try:
    option = input(f"{cmd}")
  except EOFError:
    warning()
  except KeyboardInterrupt:
    warning()

  if option == "0":
    exit("\nProgram closed\n")
  else:
    view_tools(category, category_id)

### Messagem apôs o encerramento do programa
def warning():
  exit("\n\033[31;1mProgram interrupt\033[0m\n")

def report_bugs():
  print("Report Bug")

def helper():
  print("Helper")

### Função principal
def main():
  if not check_termux_os():
    exit("Termux OS not detected")
  print("Termux OS detected")
  sleep(1)

  global total

  if isfile('toolmux.db'):
    result = tool.get_total_tool()

    if result == False:
      downloading_db()
        
    total = result.fetchall()[0][0]
    menu_options()

  else:
    downloading_db()

if __name__ == "__main__":
  main()
