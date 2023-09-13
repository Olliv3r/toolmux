from os import system

### Banner do toolmux

def banner():
    system('clear')
    banner = open('src/banner.txt', 'r')
    print(f"\033[34;1m{banner.read()}\033[0m")


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
    01) Information Collection
    02) Vulnerability Analysis
    03) Wireless Attacks
    04) Web Applications
    05) Sniffing and Faking
    06) Maintaining Access
    07) Reporting Tools
    08) Exploitation Tools
    09) Forensic Tools
    10) Stress Test
    11) Password Attacks
    12) Reverse Engineering
    13) Hardware Hacking
    14) Extra
    00) Exit
    """)
