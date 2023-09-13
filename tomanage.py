#!/usr/bin/env python
# gerenciador do toolmux
#
# Por oliver, 19 de agosto
#
#

### Importe de módulos

from src.menu import *
from src.banco import *
from os import (system, get_terminal_size)
from time import sleep

### Variáveis padronizadas

cmd = "Tomanage"
tools = Tools()
terminal_size = get_terminal_size()[1] - 4
warnning = None

### Menu gerenciar ferramentas

def menu_manager():
    banner()
    menu_manager_options() # menu importado
    
    option = input(f"{cmd}:~> ")

    if not option:
        menu_manager()

    elif option == "1" or\
         option == "01":
        menu_view_tools()

    elif option == "2" or\
         option == "02":
        menu_view_tool()

    elif option == "3" or\
         option == "03":
        menu_register_tool()
        
    elif option == "4" or\
         option == "04":
        menu_update_tool()

    elif option == "5" or\
         option == "05":
        menu_delete_tool()
        
    elif option == "6" or\
         option == "06":
        menu_do_backup()

    elif option == "7" or\
         option == "07":
        menu_import_data()

    elif option == "0" or\
         option == "00":
        exit("\nPrograma encerrado\n")
        
    else:
        menu_manager()



def menu_view_tools():
    warnning = "\n: Todas as ferramentas: \n"
    
    while True:
        banner()

        if (tools.view_total_tools() == 0):
            warnning = "\n: Não há nenhuma ferramenta : \n"
        else:
            show_tools()
        
        print(warnning)
        input("Pressione ENTER para voltar...")
        break
    
    menu_manager()
        

def menu_view_tool():
    warnning = "\n: Todas as ferramentas: \n"
    
    while True:
        print(warnning)
        banner()

        if (tools.view_total_tools() == 0):
            warnning = "\n: Não há nenhuma ferramenta : \n"
            print(warnning)
            input("Pressione ENTER para voltar...")
            menu_manager()

        else:
            show_tools()
            
            print(warnning)
            id_option = input("Informe o id da ferramenta: ")
        
            if not id_option:
                warnning = "\n: É necessário informar o id de uma ferramenta :\n"
            
            elif id_option == "back":
                option  = input("Pressione ENTER para voltar ou n para continuar nesta tela...")

                if not option:
                    menu_manager()

                elif option == "n":
                    warnning = "\n: Retorno cancelado :\n"
        
                elif not id_option.isnumeric():
                    warnning = "\n: Informe apenas números :\n"
            
            elif id_option.isnumeric() and\
                 tools.view_tool(id_option):
                banner()
            
                warnning = f"\n: Selecionou a ferramenta com id {id_option} :\n"
                print(warnning)
                show_tool(id_option)
                input("Pressione ENTER para voltar...")
                warnning = f"\n: De volta para esta tela! :\n"

            elif id_option.isnumeric() and\
                 not tools.view_tool(id_option):
                warnning = f"\n: Não existe ferramenta com o id {id_option} :\n"
    


def menu_register_tool():
    global result_category
    global result_type_install
    
    warnning = "\n: Escolha a categoria da ferramenta : \n"

    while True:
        banner()
        print(warnning)

        result_category = input_categories()
        result_type_install = input_type_install()

        previous_data_none()

        option = input("Pressione ENTER para continuar ou back para voltar...")

        if option == "back":
            menu_manager()

        if not option:
            print()
            data = input_data_register()

            if not data:
                warnning = f"\n: Preencha todos os campos! :\n"

            else:
                banner()
                previous_data_require(data)

                option = input("Pressione ENTER para confirmar ou n para cancelar...")

                if not option:
                    result = tools.register_tool(data)

                    if(result):
                        banner()
                        warnning = f"\n: Ferramenta registrada com sucesso :\n"
                        print(warnning)
                        show_tool(tools.db.cursor.lastrowid)
            
                        input("Pressione ENTER para voltar...")
                        warnning = f"\n: De volta para esta tela! :\n"

                    else:
                        warnning = f"\n: Erro ao registrar a ferramenta :\n"

                elif option == "n":
                    warnning = "\n: Retorno cancelado :\n"
        else:
            warnning = "\n: Pressione ENTER para continuar ou digite 'back' para voltar :\n"


def menu_update_tool():
    global result_category
    global result_type_install

    warnning = "\n: Escolha o id de um registro acima : \n"
    
    while True:
        banner()

        if (tools.view_total_tools() == 0):
            warnning = "\n: Não há nenhuma ferramenta : \n"
            print(warnning)
            input("Pressione ENTER para voltar...")
            menu_manager()

        else:
            show_tools()

            print(warnning)
            id_option = input("Informe o id da ferramenta: ")

            if not id_option:
                warnning = "\n: É necessário informar o id do registro :\n"

            elif id_option == "back":

                option  = input("Pressione ENTER para voltar ou n para continuar nesta tela...")

                if not option:
                
                    menu_manager()

                elif option == "n":
                    warnning = "\n: Retorno cancelado :\n"

            elif not id_option.isnumeric():
                warnning = "\n: Informe apenas números :\n"
                
            elif id_option.isnumeric() and\
                 not tools.view_tool(id_option):
                warnning = f"\n: Não existe ferramenta com o id {id_option} :\n"

            elif id_option.isnumeric() and\
                 tools.view_tool(id_option):
                banner()

                result_category = input_categories()
                result_type_install = input_type_install()

                warnning = f"\n: Selecionou a ferramenta com id {id_option} :\n"
                print(warnning)
                show_tool(id_option)

                option = input("Pressione ENTER para confirmar ou n para cancelar...")
                print()
            
                if not option:
                    data = input_data_update(id_option)
                    banner()
                    previous_data_require(data)
                    warnning = f"\n: Confirme a alteração dos dados :\n"
                    print(warnning)
                    option  = input("Pressione ENTER para continuar ou n para para cancelar...")

                    if not option:

                        result = tools.update_tool(data, id_option)
                        if result == True:
                            banner()
                            warnning = f"\n: Ferramenta atualizada com sucesso {result} :\n"
                            print(warnning)
                            show_tool(id_option)
                            input("Pressione ENTER para voltar...")
                            warnning = f"\n: De volta para esta tela! :\n"
                    
                        else:
                            warnning = f"\n: Erro ao atualizar a ferramenta {result} :\n"

                    elif option == "n":
                        warnning = "\n: Ação cancelada :\n"
                        
                elif  option == "n":
                    warnning = "\n: Retorno cancelado :\n"
                

def menu_delete_tool():
    warnning = "\n: Escolha o id de um registro acima : \n"
    
    while True:
        banner()

        if (tools.view_total_tools() == 0):
            warnning = "\n: Não há nenhuma ferramenta : \n"
            print(warnning)
            input("Pressione ENTER para voltar...")
            menu_manager()

        else:
            show_tools()

            print(warnning)
            id_option = input("Informe o id da ferramenta: ")

            if not id_option:
                warnning = "\n: É necessário informar o id do registro :\n"
                
            elif id_option == "back":

                option  = input("Pressione ENTER para voltar ou n para continuar nesta tela...")

                if not option:
                
                    menu_manager()

                elif option == "n":
                    warnning = "\n: Retorno cancelado :\n"

            elif not id_option.isnumeric():
                warnning = "\n: Informe apenas números :\n"

            elif id_option.isnumeric() and\
                 not tools.view_tool(id_option):
                warnning = f"\n: Não existe ferramenta com o id {id_option} :\n"

            elif id_option.isnumeric() and\
                 tools.view_tool(id_option):
                banner()
                warnning = f"\n: Selecionou a ferramenta com id {id_option} :\n"
                print(warnning)
                show_tool(id_option)

                warnning = f"\n: Confirme a exclusão da ferramenta :\n"
                print(warnning)
                option = input("Pressione ENTER para confirmar ou n para cancelar...")
                print()
            
                if not option:
                    
                    result = tools.delete_tool(id_option)
                    
                    if(result):
                        banner()
                        warnning = f"\n: Ferramenta excluída com sucesso :\n"
                        print(warnning)
                    
                        input("Pressione ENTER para voltar...")
                        warnning = f"\n: De volta para esta tela! :\n"
                    
                    else:
                        warnning = f"\n: Erro ao excluir a ferramenta :\n"

                elif option == "n":
                    warnning = "\n: Ação cancelada :\n"


def menu_do_backup():
    warnning = "\n: Fazer backup : \n"
    
    while True:
        banner()
        print(warnning)
        option = input("Pressione ENTER para confirmar ou back para voltar...")

        if not option:
            result = tools.do_backup()

            if result == True:
                warnning = "\n: Backup realizado em sql/tools.sql: \n"
            else:
                warnning = f"\n: Erro ao reaizar o backup {result} : \n"

        elif option == "back":
            menu_manager()

def menu_import_data():
    warnning = "\n: Importar dados : \n"
    
    while True:
        banner()
        print(warnning)
        option = input("Pressione ENTER para confirmar ou back para voltar...")
        if not option:

            result = tools.import_data()

            try:
                if result == True:
                    warnning = "\n: Dados importados de sql/tools.sql: \n" 
                else:
                    warnning = f"\n: Erro ao importar os dados, o {tools.db.db_name} já existe. Exclua primeiro. :\n"

            except FileNotFoundError as err:
                warnning = f"\n: {err} :\n"

        elif option == "back":
            menu_manager()
                       
### Mostra dados de todos as ferramentas atravé da tabela

def show_tools():
    result = tools.view_tools()
    
    try:
        for tool in result:
            show_tool(tool[0])

        return True
    
    except TypeError as err:
        print(f"\n: {err} :")
        return False


### Mostra dados de uma ferramenta através do ID

def show_tool(ID):
    print("-"*terminal_size*2)
    
    for column_value in tools.view_tool(ID):
        print(f": Pacote : {column_value[1]}")
        print(f":")
        print(f": Id : {column_value[0]}")
        print(f": Nome : {column_value[1]}")
        print(f": Apelido : {column_value[2]}")
        print(f": Link : {column_value[3]}")
        print(f": Categoria : {column_value[4]}")
        print(f": Dependencias : {column_value[5]}")
        print(f": Nome do instalador : {column_value[6]}")
        print(f": Instalação via : {column_value[7]}")

    print("-"*terminal_size*2)

    
### Prévia dos dados preenchidos nos campos

def previous_data_require(data):
    print("-"*terminal_size*2)
    print(f": Pacote : {data[0]}")
    print(f":")
    print(f": Nome : {data[0]}")
    print(f": Apelido : {data[1]}")
    print(f": Link : {data[2]}")
    print(f": Categoria : {data[3]}")
    print(f": Dependencias : {data[4]}")
    print(f": Nome do instalador : {data[5]}")
    print(f": Instalação via : {data[6]}")
    print("-"*terminal_size*2)


### Prévia dos campos preenchidos

def previous_data_none():
    banner()
    print("\n: Exemplo de dados necessários :\n")
    print("-"*terminal_size*2)
    print(f": Pacote : Setoolkit")
    print(f":")
    print(f": Nome : Setoolkit")
    print(f": Apelido : setoolkit")
    print(f": Link : https://github.com/trustedsec/social-engineer-toolkit")
    print(f": Categoria : information_collection")
    print(f": Dependencias : git python2")
    print(f": Nome do instalador : ")
    print(f": Instalação via : apt")
    print("-"*terminal_size*2)


### Pede dados na entrada

def input_data_register():
    data = []

    category = result_category
    type_install = result_type_install
     
    name = input(f"{cmd}-[Nome]:~> ")
    alias = input(f"{cmd}-[Apelido]:~> ")
    link = input(f"{cmd}-[Link: repo OU instalador]:~> ")
    dependencies = input(f"{cmd}-[Dependências sepadas por spaços]:~> ")
    name_installer = input(f"{cmd}-[Name installer: msfinstall ou vazío]:~> ")

    for inpu in name,\
        alias,\
        link,\
        category,\
        dependencies,\
        name_installer,\
        type_install:
        data.append(inpu)
        
    return data

def input_data_update(ID):
    result = tools.view_tool(ID)

    category = result_category
    type_install = result_type_install

    data_defa = []
    data = []

    if result:

        for r in result:
            data_defa.append(r)
    
        name = input(f"{cmd}-[Nome]:~> ")
        if name == "":
            name = data_defa[0][1]
 
        alias = input(f"{cmd}-[Apelido]:~> ")
        if alias == "":
            alias = data_defa[0][2]
    
        link = input(f"{cmd}-[Link: Repo ou instalador]:~> ")
        if link == "":
            link = data_defa[0][3]
    
        #category = input(f"{cmd}-[Categoria]:~> ")
        if not category:
            category = data_defa[0][4]
    
        dependencies = input(f"{cmd}-[Dependências separadas por espaços]:~> ")
        if dependencies == "":
            dependencies = data_defa[0][5]

        name_installer = input(f"{cmd}-[Name installer: msfinstall ou vazíu]:~> ")
        if name_installer == "":
            name_installer = data_defa[0][6]
    
        #type_install = input(f"{cmd}-[Instalação via]:~> ")
        if not type_install:
            type_install = data_defa[0][7]

        data.append(name)
        data.append(alias)
        data.append(link)
        data.append(category)
        data.append(dependencies)
        data.append(name_installer)
        data.append(type_install)
        
        return data
    
    else:
        return False


def input_categories():
    banner()
    print("\n: Selecione a categoria da ferramenta que será cadastrada :\n")
    
    categories = ["information_collection",
            "vulnerability_analysis",
            "wireless_attacks",
            "web_applications",
            "sniffing_and_faking",
            "maintaining_access",
            "reporting_tools",
            "exploitation_tools",
            "forensic_tools",
            "stress_test",
            "password_attacks",
            "reverse_engineering",
            "hardware_hacking",
            "extra"]

    c = 1

    for i in categories:
        print(f"\t{c} {i.replace('_', ' ').capitalize()}")
        c = c + 1


    print()
    category_option = input("Categoria: ")
    

    if category_option == "back":
        menu_manager()

    elif not category_option:
        print("\n: É necessário escolher a categoria da ferramenta : \n")
        input("ENTER para voltar...")
        input_categories()

    elif not category_option.isnumeric() or\
         int(category_option) == 0:
        print("\n: Digite somente os números disponíveis acima : \n")
        input("ENTER para voltar...")
        input_categories()

    else:
        try:
            result_category_option = find_item_index(category_option, categories)
            return result_category_option
        
        except IndexError as err:
            print(f"\n: Não existe categoria com o índice {category_option} - erro '{err}' :\n")
            input("ENTER para voltar...")
            input_categories()
        

def input_type_install():
    banner()
    print("\n: Selecione o meio de instalação da ferramenta :\n")
    
    types_install = ["apt",
        "apt not official",
        "git",
        "wget"]

    c = 1

    for i in types_install:
        print(f"\t{c} {i.capitalize()}")
        c = c + 1


    print()
    type_install_option = input("Instalação via: ")


    if type_install_option == "back":
        menu_register_tool()
    
    elif not type_install_option:
        print("\n: É necessário escolher o modo de instalação da ferramenta : \n")
        input("ENTER para voltar...")
        input_type_install()

    elif not type_install_option.isnumeric() or\
         int(type_install_option) == 0:
        print("\n: Digite somente os números disponíveis acima : \n")
        input("ENTER para voltar...")
        input_type_install()

    else:
        try:
            result_type_install_option = find_item_index(type_install_option, types_install)
            return result_type_install_option
        
        except IndexError as err:
            print(f"\n: Não existe modo com o índice {type_install_option} - erro '{err}' :\n")
            input("ENTER para voltar...")
            input_type_install()


    
def find_item_index(item_arg, list_arg):
    list_items = list_arg
    list_items_index = []

    for item in list_items:
        list_items_index.append(list_items.index(item))

    if len(item_arg) in list_items_index:
        return list_items[int(item_arg) -1]
    else:
        return False

    
menu_manager()
