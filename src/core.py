import src.ui_handlers as ui
import src.file_handlers as file_io
# import datetime
from src.constants import COURIERS_KEYS, PRODUCTS_KEYS, ORDERS_KEYS

#Initialize mainMenu
mainMenu = ui.import_Menu("mainMenu", "Main Menu")
def print_Main_Menu():
    ui.c_Print(mainMenu)

#Initialize mainMenu prompt
main_Menu_options = ui.initialize_Prompt_Completer_From_Menu("mainMenu")
prompt_text = "Choose/type an option:"
def prompt_Main_Menu():
    user_input = ui.prompt_User(prompt_text, main_Menu_options)
    return user_input

#Initialize subMenu for couriers and products
couriers_menu = ui.import_Menu("subMenu", "Couriers")
products_menu = ui.import_Menu("subMenu", "Products")
def print_sub_menu(name):
    if name == "couriers":
        ui.c_Print(couriers_menu)
    elif name == "products":
        ui.c_Print(products_menu)

#Initialize subMenu prompt
# sub_menu_options_list = ui.import_List_Options("submenu")
# sub_menu_options = ui.initialize_Prompt_Completer(sub_menu_options_list)
sub_menu_options = ui.initialize_Prompt_Completer_From_Menu("subMenu")
def prompt_sub_menu():
    user_input = ui.prompt_User(prompt_text, sub_menu_options)
    return user_input

#Initialize database
state = {
    "couriers": file_io.read_Table("couriers"),
    "products": file_io.read_Table("products"),
    "orders": file_io.read_Table("orders")
}

#Initialize yes/no completer
yes_no_completer = ui.initialize_Prompt_Completer(["yes", "no"])

#Save database
def save_state(state):
    file_io.write_Table("couriers", state["couriers"], COURIERS_KEYS)
    file_io.write_Table("products", state["products"], PRODUCTS_KEYS)
    file_io.write_Table("orders", state["orders"], ORDERS_KEYS)
    # for each_table in state.keys():
    #     file_io.write_Table(each_table, state[each_table])

#Saving database routine
def save_option(state):
    save_state(state)
    ui.clear_Term()
    ui.c_Print("Saved")
    ui.prompt_User("Press Enter")

#Main menu options if-else
def main_menu():
    while True:
        ui.clear_Term()
        print_Main_Menu()
        user_input = prompt_Main_Menu()
        if user_input == "couriers" or user_input == "products":
            sub_menu(state, user_input)
        elif user_input == "save":
            save_option(state)
        elif user_input == "exit":
            ui.clear_Term()
            if not ui.prompt_User("Would you not like to save?\n", yes_no_completer) == "no":
                save_option(state)
            ui.clear_Term()
            exit()

#Sub menu options if-else
def sub_menu(state, table):
    while True:
        ui.clear_Term()
        print_sub_menu(table)
        user_input = prompt_sub_menu()
        if user_input == "show":
            ui.clear_Term()
            ui.print_table(state, table)
            ui.prompt_User("Press Enter")
        elif user_input == "return":
            break