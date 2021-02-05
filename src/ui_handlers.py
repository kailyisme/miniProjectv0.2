import csv
import os
from rich.table import Table
from rich.console import Console
from rich.style import Style
# from prompt_toolkit.shortcuts.prompt import PromptSession
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from src.constants import COURIERS_KEYS, PRODUCTS_KEYS

#Rich Console Style
c_Style = Style(bgcolor= "thistle1", color="black")
#Rich Console Initializer
c = Console()

#Initialize print function with custom c_Style
def c_Print(what_To_Print):
    c.print(what_To_Print, style=c_Style, justify="center")

#Read menu from file
def read_Menu(name_Of_Menu:str):
    path_Of_Menu = f"data/{name_Of_Menu}.menu"
    with open(path_Of_Menu) as file:
        csv_Reader = csv.reader(file)
        whole_Menu = [rows for rows in csv_Reader]
        menu_Headers = whole_Menu[0]
        menu_Body = whole_Menu[1:]
    return menu_Headers, menu_Body

#Assemble menu from read menu
def import_Menu(name_Of_Menu:str, title:str):
    #Importing menu from file (csv)
    menu_Headers, menu_Body = read_Menu(name_Of_Menu)
    #Construct Rich Table of the Menu
    menu = Table(title = title)
    for header in menu_Headers:
        menu.add_column(header, justify = "center", no_wrap = True)
    for each_Row in menu_Body:
        menu.add_row(*each_Row)
    return menu

#Import menu options from file
def import_List_Options(name_Of_Table:str, read_Menu=read_Menu):
    to_Discard, menu_Body = read_Menu(name_Of_Table)
    list_of_options = [each[0] for each in menu_Body]
    return list_of_options

#Clear console
def clear_Term():
    os.system('cls' if os.name == 'nt' else 'clear')

# To enable prompt history
# def initialize_prompt_session():
#     prompt_Session = PromptSession()
#     return prompt_Session

#Initialize prompt completer from list of options
def initialize_Prompt_Completer(words_expected:list):
    word_completer = WordCompleter(words_expected)
    return word_completer

#Initialize prompt completer directly from menu file
def initialize_Prompt_Completer_From_Menu(name_Of_Menu:str):
    to_Discard, menu_Body = read_Menu(name_Of_Menu)
    words_expected = [each[0] for each in menu_Body]
    word_completer = WordCompleter(words_expected)
    return word_completer

#Initialize a user prompt
def prompt_User(prompt_Text="", my_completer=WordCompleter([]), prompt=prompt):
    # user_Input = prompt_Session.prompt(f"{promptText} >")
    user_Input = prompt(f"{prompt_Text} >", completer=my_completer, complete_while_typing=True)
    return user_Input.strip()

#Assemble a grid for formatting
# def assemble_grid(*list_elements):
#     grid = Table.grid(expand = True)
#     number_of_elements = len(list_elements)
#     for each in range(number_of_elements):
#         if each == (number_of_elements - 1):    #if last column then align to the right
#             grid.add_column(justify="right")
#         else:
#             grid.add_column(justify="centre")
#     grid.add_column(*list_elements)

#View a table function
def print_table(state, table_name):
    keys = []
    if table_name == "couriers":
        keys = COURIERS_KEYS
    elif table_name == "products":
        keys = PRODUCTS_KEYS
    table = Table(title=table_name)
    for each in keys:
        table.add_column(each, justify = "center", no_wrap = True)
    for line in state[table_name]:
        row = []
        for key in keys:
            row.append(line[key])
        table.add_row(*row)
    c_Print(table)