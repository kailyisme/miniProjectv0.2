import src.ui_handlers as ui
import src.file_handlers as file_io
import src.db_handlers as db
import src.constants as constants
# from uuid import UUID, uuid4
# import datetime


# Initialize mainMenu
mainMenu = ui.import_Menu("mainMenu", "Main Menu")


def print_Main_Menu():
    ui.c_Print(mainMenu)


# Initialize mainMenu prompt
main_Menu_options = ui.initialize_Prompt_Completer_From_Menu("mainMenu")
prompt_text = "Choose/type an option:"


def prompt_Main_Menu():
    user_input = ui.prompt_User(prompt_text, main_Menu_options)
    return user_input


# Initialize subMenu for couriers and products and customers
courier_menu = ui.import_Menu("subMenu", "Courier")
product_menu = ui.import_Menu("subMenu", "Product")
customer_menu = ui.import_Menu("subMenu", "Customer")


def print_sub_menu(name):
    if name == "courier":
        ui.c_Print(courier_menu)
    elif name == "product":
        ui.c_Print(product_menu)
    elif name == "customer":
        ui.c_Print(customer_menu)


# Initialize subMenu prompt
sub_menu_options = ui.initialize_Prompt_Completer_From_Menu("subMenu")


def prompt_sub_menu():
    user_input = ui.prompt_User(prompt_text, sub_menu_options)
    return user_input


# Initialize orderMenu
orderMenu = ui.import_Menu("orderMenu", "Order")


def print_order_menu():
    ui.c_Print(orderMenu)


# Initialize orderMenu prompt
order_menu_options = ui.initialize_Prompt_Completer_From_Menu("orderMenu")


def prompt_order_menu():
    user_input = ui.prompt_User(prompt_text, order_menu_options)
    return user_input


# Initialize MySQL DB connection
conn = db.connection()

# Initialize database
state = {
    table_name: db.select_all_from_table(conn, table_name)
    for table_name in constants.TABLE_NAMES
}

# Initialize yes/no completer
yes_no_completer = ui.initialize_Prompt_Completer(["yes", "no"])

# Saving database routine to CSV
def save_option(state):
    file_io.save_state(state)
    ui.clear_Term()
    ui.c_Print("Saved to data")
    ui.prompt_User("Press Enter")


# Main menu options if-else
def main_menu():
    while True:
        ui.clear_Term()
        print_Main_Menu()
        user_input = prompt_Main_Menu()
        if (
            user_input == "courier"
            or user_input == "product"
            or user_input == "customer"
        ):
            sub_menu(state, user_input)
        elif user_input == "order":
            order_menu(state)
        elif user_input == "save":
            save_option(state)
        elif user_input == "exit":
            ui.clear_Term()
            exit()


def add_row_to_table(table_name):
    ui.clear_Term()
    ui.c_Print(f"Please input the following details for a new {table_name}")
    new_row = ui.prompt_row(table_name)
    db.insert_into_table(conn, table_name, new_row)
    state[table_name].append(db.get_highest_id(conn, table_name))
    ui.clear_Term()
    ui.c_Print(f"Appended {state[table_name][-1]}")
    ui.prompt_User("Press Enter")


def update_row_on_table(table_name):
    ui.clear_Term()
    ui.print_table(state[table_name], table_name, True)
    row_index = None
    while not row_index in range(len(state[table_name])):
        row_index = int(ui.prompt_User("Which row number would you like to update"))
    ui.clear_Term()
    ui.c_Print(f"Please input new details for {state[table_name][row_index]}")
    new_row = ui.prompt_update_row(state, table_name, row_index)
    row_id = state[table_name][row_index][f"{table_name}_id"]
    db.update_row_on_table(conn, table_name, new_row, row_id)
    state[table_name][row_index] = db.retrieve_row_for_id(conn, table_name, row_id)
    ui.clear_Term()
    ui.c_Print(f"Updated row {state[table_name][row_index]}")
    ui.prompt_User("Press Enter")


def remove_row_from_table(table_name):
    ui.clear_Term()
    ui.print_table(state[table_name], table_name, True)
    row_index = None
    while not row_index in range(len(state[table_name])):
        row_index = int(ui.prompt_User("Which row number would you like to remove"))
    ui.clear_Term()
    row_id = state[table_name][row_index][f"{table_name}_id"]
    ui.c_Print(
        f"You sure you would like to remove ",
        db.retrieve_row_for_id(conn, table_name, row_id),
    )
    if ui.prompt_User("Yes/No", yes_no_completer) == "yes":
        ui.clear_Term()
        db.delete_row_for_id(conn, table_name, row_id)
        ui.c_Print("Removed ", state[table_name].pop(row_index))
        ui.prompt_User("Press Enter")


# Sub menu options if-else
def sub_menu(state, table_name):
    while True:
        ui.clear_Term()
        print_sub_menu(table_name)
        user_input = prompt_sub_menu()
        if user_input == "show":
            ui.clear_Term()
            ui.print_table(state[table_name], table_name)
            ui.prompt_User("Press Enter")
        elif user_input == "add":
            add_row_to_table(table_name)
        elif user_input == "update":
            update_row_on_table(table_name)
        elif user_input == "remove":
            remove_row_from_table(table_name)
        elif user_input == "return":
            break


def order_menu(state):
    while True:
        ui.clear_Term()
        print_order_menu()
        user_input = prompt_order_menu()
        if user_input == "show":
            ui.clear_Term()
            ui.print_table(state["transaction"], "transaction")
            ui.prompt_User("Press Enter")
        elif user_input == "return":
            break