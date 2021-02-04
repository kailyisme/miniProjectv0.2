import src.ui_handlers as ui
import src.file_handlers as file_io
import os
# import datetime

#Table keys
COURIERS_KEYS = ["name","phone"]
PRODUCTS_KEYS = ["name","price"]
ORDERS_KEYS = ["time","customer_name","customer_address","customer_phone","courier","status","items"]

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
sub_menu_options_list = ui.import_List_Options("submenu")
sub_menu_options = ui.initialize_Prompt_Completer(sub_menu_options_list)
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

def save_state(state):
    file_io.write_Table("couriers", state["couriers"], COURIERS_KEYS)
    file_io.write_Table("products", state["products"], PRODUCTS_KEYS)
    file_io.write_Table("orders", state["orders"], ORDERS_KEYS)
    # for each_table in state.keys():
    #     file_io.write_Table(each_table, state[each_table])

def save_option():
    save_state(state)
    ui.clear_Term()
    ui.c_Print("Saved")
    ui.prompt_User("Press Enter")

def main_menu_logic(user_input):
    if user_input == "save":
        save_option()
    elif user_input == "exit":
        ui.clear_Term()
        if not ui.prompt_User("Would you not like to save?\n", yes_no_completer) == "no":
            save_option()
        ui.clear_Term()
        exit()