from os import system
from random import choice

### Banner do toolmux

def banner():
    system('clear')
    banner = open('src/banner.txt', 'r')
    print(banner.read())


### Menu de opçôes do gerenciador

def menu_manager_options():
    print("""
    1) Ver todas as ferramentas
    2) Ver uma ferramenta
    3) Cadastrar uma ferramenta
    4) Atualizar uma ferramenta
    5) Deletar uma ferramenta
    6) Fazer backup
    7) Importar dados
    0) Sair do tomanage
    """)

### Menu de categorias das ferramentas

def menu_tools_categories():
    print("""
    1) Information Collection
    2) Vulnerability Analysis
    3) Wireless Attacks
    4) Web Applications
    5) Sniffing and Faking
    6) Maintaining Access
    7) Reporting Tools
    8) Exploration Tools
    9) Forensic Tools
    10) Stress Test
    11) Password Attacks
    12) Reverse Engineering
    13) Hardware Hacking
    14) Extra
    0) Exit
    """)
