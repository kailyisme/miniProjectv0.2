import csv
import os
from rich.table import Table
from rich.console import Console
from rich.style import Style
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import src.constants as constants
import uuid


# Rich Console Style
c_Style = Style(bgcolor="thistle1", color="black")
# Rich Console Initializer
c = Console()

# Initialize print function with custom c_Style
def c_Print(*what_To_Print):
    c.print(*what_To_Print, style=c_Style, justify="center")


# Read menu from file
def read_Menu(name_Of_Menu: str):
    path_Of_Menu = f"data/{name_Of_Menu}.menu"
    with open(path_Of_Menu) as file:
        csv_Reader = csv.reader(file)
        whole_Menu = [rows for rows in csv_Reader]
        menu_Headers = whole_Menu[0]
        menu_Body = whole_Menu[1:]
    return menu_Headers, menu_Body


# Assemble menu from read menu
def import_Menu(name_Of_Menu: str, title: str):
    # Importing menu from file (csv)
    menu_Headers, menu_Body = read_Menu(name_Of_Menu)
    # Construct Rich Table of the Menu
    menu = Table(title=title)
    for header in menu_Headers:
        menu.add_column(header, justify="center", no_wrap=True)
    for each_Row in menu_Body:
        menu.add_row(*each_Row)
    return menu


# Import menu options from file
def import_List_Options(name_Of_Table: str, read_Menu=read_Menu):
    to_Discard, menu_Body = read_Menu(name_Of_Table)
    list_of_options = [each[0] for each in menu_Body]
    return list_of_options


# Clear console
def clear_Term():
    os.system("cls" if os.name == "nt" else "clear")


# Initialize prompt completer from list of options
def initialize_Prompt_Completer(words_expected: list):
    word_completer = WordCompleter(words_expected)
    return word_completer


# Initialize prompt completer directly from menu file
def initialize_Prompt_Completer_From_Menu(name_Of_Menu: str):
    to_Discard, menu_Body = read_Menu(name_Of_Menu)
    words_expected = [each[0] for each in menu_Body]
    word_completer = WordCompleter(words_expected)
    return word_completer


# Initialize a user prompt
def prompt_User(prompt_Text="", my_completer=WordCompleter([]), prompt=prompt):
    user_Input = prompt(
        f"{prompt_Text} >", completer=my_completer, complete_while_typing=True
    )
    return user_Input.strip()


# View a table function
def print_table(table_to_print, table_name, enum=False, keys=[]):
    if keys == []:
        keys = constants.get_keys(table_name)
    table = Table(title=table_name)
    if enum == False:
        for each in keys:
            table.add_column(each, justify="center", no_wrap=True)
        for line in table_to_print:
            row = []
            for key in keys:
                if len(key.split("_")) > 1 and key.split("_")[1] == "uuid":
                    row.append(str(uuid.UUID(bytes=line[key])))
                else:
                    try:
                        row.append(str(line[key]))
                    except:
                        row.append(None)
            table.add_row(*row)
    else:
        table.add_column("#", justify="center", no_wrap=True)
        for each in keys:
            table.add_column(each, justify="center", no_wrap=True)
        for num, line in enumerate(table_to_print):
            row = [str(num)]
            for key in keys:
                if len(key.split("_")) > 1 and key.split("_")[1] == "uuid":
                    row.append(str(uuid.UUID(bytes=line[key])))
                else:
                    try:
                        row.append(str(line[key]))
                    except:
                        row.append(None)
            table.add_row(*row)
    c_Print(table)


# Prompt user for row details
def prompt_row_wo_refs(table_name):
    keys = constants.get_keys(table_name)
    ignored_keys = [f"{table_name}_id", f"{table_name}_uuid"]
    row = {}
    for key in keys:
        if key not in ignored_keys:
            user_input = prompt_User(key)
            if user_input != "":
                row[key] = user_input
    return row


# Prompt user for order details
def prompt_row_for_order(customer_table, courier_table):
    row = {}
    print_table(customer_table, "customer", True)
    row["customer_index"] = None
    while row["customer_index"] not in range(len(customer_table)):
        row["customer_index"] = int(prompt_User("Which customer #"))
    clear_Term()
    print_table(courier_table, "courier", True)
    row["courier_index"] = None
    while row["courier_index"] not in range(len(courier_table)):
        row["courier_index"] = int(prompt_User("Which courier #"))
    return row


# Prompt user for updated row details
def prompt_update_row(state, table_name, index):
    keys = constants.get_keys(table_name)
    keys = [each for each in keys if each != f"{table_name}_id"]
    row = {}
    for each in keys:
        user_input = prompt_User(
            each, initialize_Prompt_Completer([state[table_name][index][each]])
        )
        if user_input == "":
            pass
        else:
            row[each] = user_input
    return row


# Print basket for a transaction
def print_basket_for_transaction(basket_table, product_table, transaction_uuid):
    title = f"Basket for {uuid.UUID(bytes=transaction_uuid)}"
    keys = ["product_id", "Product name", "Amount", "Product price"]
    table_rows = []
    basket_price = 0
    for line in [
        line for line in basket_table if line["transaction_uuid"] == transaction_uuid
    ]:
        row = {}
        x_price = 0
        x_amount = 0
        row["product_id"] = str(line["product_id"])
        for product in product_table:
            if product["product_id"] == line["product_id"]:
                row["Product name"] = str(product["product_name"])
                row["Product price"] = str(product["product_price"])
                x_price = product["product_price"]
                break
        row["Amount"] = str(line["basket_amount"])
        x_amount = line["basket_amount"]
        basket_price += x_amount * x_price
        table_rows.append(row)
    table_rows.append({f"{keys[2]}": "BASKET PRICE/SUM:", f"{keys[3]}": str(basket_price)})
    print_table(table_rows, title, False, keys)