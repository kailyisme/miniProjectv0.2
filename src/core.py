import src.ui_handlers as ui
import src.file_handlers as file_io
import src.db_handlers as db
import src.constants as constants

# import uuid
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


# Initialize basketMenu
basketMenu = ui.import_Menu("basketMenu", "Basket")


def print_basket_menu():
    ui.c_Print(basketMenu)


# Initialize basketMenu prompt
basket_menu_options = ui.initialize_Prompt_Completer_From_Menu("basketMenu")


def prompt_basket_menu():
    user_input = ui.prompt_User(prompt_text, basket_menu_options)
    return user_input

# Initialize order statuses completer
order_status_options = ui.initialize_Prompt_Completer(constants.TRANSACTION_STATUSES)

# Initialize order statuses table
def print_statuses_options():
    table_name = "Order Status Options"
    table_to_print = []
    for status in constants.TRANSACTION_STATUSES:
        table_to_print.append({"Status": status})
    ui.print_table(table_to_print, table_name, False, ["Status"])

# Initialize MySQL DB connection
conn = db.connection()

# Initialize database
def init():
    return {
        table_name: list(db.select_all_from_table(conn, table_name))
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


def load_option(state):
    ui.clear_Term()
    ui.c_Print(
        "Please save the files you would like to import in a folder with the name 'to_import' in the app folder"
    )
    ui.prompt_User("Press Enter when ready...")
    temp_state = {
        table_name: file_io.read_Table(table_name)
        for table_name in constants.TABLE_NAMES
    }
    files_found = []
    for table_name in constants.TABLE_NAMES:
        if temp_state[table_name] != []:
            skip = False
            for key in constants.get_keys(table_name):
                if key not in list(temp_state[table_name][0].keys()):
                    skip = True
                    break
            if skip == True:
                continue
            ui.c_Print(f"Found {table_name}.csv")
            files_found.append(table_name)
    ui.c_Print(f"Found {len(files_found)} files")
    # ui.c_Print(temp_state)
    if (
        ui.prompt_User(
            "Are you sure you want to import these files? RISK OF ERASING OLD VALUES (yes/no)",
            yes_no_completer,
        ).lower()
        == "yes"
    ):
        for table_name in files_found:
            for entry in temp_state[table_name]:
                row = {}
                for key in constants.get_keys(table_name):
                    if entry[key] != "" and entry[key] != None:
                        row[key] = entry[key]
                db.replace_into_table(conn, table_name, row)
        state = init()
        ui.clear_Term()
        ui.c_Print("Imported!")
        ui.prompt_User("Press Enter")
    return state


def add_row_to_table(state, table_name):
    ui.clear_Term()
    ui.c_Print(f"Please input the following details for a new {table_name}")
    new_row = ui.prompt_row_wo_refs(table_name)
    db.insert_into_table(conn, table_name, new_row)
    state[table_name].append(db.get_highest_id(conn, table_name))
    ui.clear_Term()
    ui.c_Print(f"Appended {state[table_name][-1]}")
    ui.prompt_User("Press Enter")
    return state


def update_row_on_table(state, table_name):
    ui.clear_Term()
    ui.print_table(state[table_name], table_name, True)
    row_index = ui.prompt_user_row_index(state[table_name], table_name)
    ui.clear_Term()
    ui.c_Print(f"Please input new details for {state[table_name][row_index]}")
    new_row = ui.prompt_update_row(state, table_name, row_index)
    row_id = state[table_name][row_index][f"{table_name}_id"]
    db.update_row_on_table(conn, table_name, new_row, row_id)
    state[table_name][row_index] = db.retrieve_row_for_id(conn, table_name, row_id)
    ui.clear_Term()
    ui.c_Print(f"Updated row {state[table_name][row_index]}")
    ui.prompt_User("Press Enter")
    return state


def remove_row_from_table(state, table_name):
    ui.clear_Term()
    ui.print_table(state[table_name], table_name, True)
    row_index = ui.prompt_user_row_index(state[table_name], table_name)
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
    return state


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
            state = add_row_to_table(state, table_name)
        elif user_input == "update":
            state = update_row_on_table(state, table_name)
        elif user_input == "remove":
            state = remove_row_from_table(state, table_name)
        elif user_input == "return":
            return state


# Add a basket to a transaction
def add_basket(state, transaction_uuid):
    basket_entry = {}
    basket_entry["transaction_uuid"] = transaction_uuid
    user_input = "yes"
    while user_input == "yes":
        ui.clear_Term()
        ui.print_table(state["product"], "product", True)
        product_index = ui.prompt_user_row_index(state["product"], "product")
        basket_entry["product_id"] = state["product"][product_index]["product_id"]
        ui.clear_Term()
        ui.c_Print(f"How many {state['product'][product_index]['product_name']}?")
        basket_entry["basket_amount"] = int(ui.prompt_User())
        db.insert_into_table(conn, "basket", basket_entry)
        state["basket"].append(db.get_highest_id(conn, "basket"))
        ui.clear_Term()
        ui.c_Print(f"Appended {state['basket'][-1]}")
        user_input = ui.prompt_User(
            "Would you like to add another product to the basket? (yes/no)",
            yes_no_completer,
        ).lower()
    return state


def add_order(state):
    ui.clear_Term()
    new_row = ui.prompt_row_for_order(state["customer"], state["courier"])
    db.new_order(
        conn,
        state["customer"][new_row["customer_index"]]["customer_id"],
        state["courier"][new_row["courier_index"]]["courier_id"],
    )
    state["transaction"].append(db.get_most_recent_order(conn))
    ui.clear_Term()
    ui.c_Print(f"Appended {state['transaction'][-1]}")
    if (
        ui.prompt_User(
            "Would you like to add a basket? (yes/no)", yes_no_completer
        ).lower()
        == "yes"
    ):
        state = add_basket(state, state["transaction"][-1]["transaction_uuid"])
    return state

# Change an order status
def change_order_status(state):
    ui.clear_Term()
    ui.print_table(state["transaction"], "transaction", True)
    transaction_index = ui.prompt_user_row_index(state["transaction"], "transaction")
    transaction_uuid = state["transaction"][transaction_index]["transaction_uuid"]
    ui.clear_Term()
    print_statuses_options()
    new_status = ui.prompt_User("Type status wanted", order_status_options)
    while new_status not in constants.TRANSACTION_STATUSES:
        new_status = ui.prompt_User("Type a valid status", order_status_options)
    new_status = {"transaction_status": new_status}
    db.update_row_on_table(conn, "transaction", new_status, transaction_uuid, True)
    state["transaction"][transaction_index] = db.retrieve_row_for_id(conn, "transaction", transaction_uuid, True)
    ui.clear_Term()
    ui.c_Print(f"Updated: {state['transaction'][transaction_index]}")
    ui.prompt_User("Press Enter")
    return state

# Order menu options if-else
def order_menu(state):
    while True:
        ui.clear_Term()
        print_order_menu()
        user_input = prompt_order_menu()
        if user_input == "show":
            ui.clear_Term()
            ui.print_table(state["transaction"], "transaction")
            ui.prompt_User("Press Enter")
        elif user_input == "add":
            state = add_order(state)
        elif user_input == "basket":
            state = basket_menu(state)
        elif user_input == "change":
            state = change_order_status(state)
        elif user_input == "return":
            return state


# Show basket
def show_basket(state):
    ui.print_table(state["transaction"], "transaction", True)
    row_index = ui.prompt_user_row_index(state["transaction"], "transaction")
    ui.clear_Term()
    ui.print_basket_for_transaction(
        state["basket"],
        state["product"],
        state["transaction"][row_index]["transaction_uuid"],
    )
    ui.prompt_User("Press Enter")


# Add to existing basket
def add_to_basket(state):
    ui.print_table(state["transaction"], "transaction", True)
    transaction_index = ui.prompt_user_row_index(state["transaction"], "transaction")
    add_basket(state, state["transaction"][transaction_index]["transaction_uuid"])
    return state


# Basket menu options if-else
def basket_menu(state):
    while True:
        ui.clear_Term()
        print_basket_menu()
        user_input = prompt_basket_menu()
        if user_input == "show":
            ui.clear_Term()
            if state["transaction"] == []:
                ui.c_Print("THERE ARE NO TRANSACTIONS TO SHOW")
                continue
            show_basket(state)
        elif user_input == "add":
            ui.clear_Term()
            if state["transaction"] == []:
                ui.c_Print("THERE ARE NO TRANSACTIONS TO SHOW")
                continue
            state = add_to_basket(state)
        elif user_input == "return":
            return state


# Main menu options if-else
def main_menu(state):
    while True:
        ui.clear_Term()
        print_Main_Menu()
        user_input = prompt_Main_Menu()
        if (
            user_input == "courier"
            or user_input == "product"
            or user_input == "customer"
        ):
            state = sub_menu(state, user_input)
        elif user_input == "order":
            state = order_menu(state)
        elif user_input == "save":
            save_option(state)
        elif user_input == "load":
            state = load_option(state)
        elif user_input == "exit":
            ui.clear_Term()
            exit()