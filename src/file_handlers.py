import csv
import src.ui_handlers as ui
from src.constants import COURIERS_KEYS, PRODUCTS_KEYS, ORDERS_KEYS

#Read table from CSV file
def read_Table(name_Of_Table:str):
    the_Table = []
    path_Of_Table = f"data/{name_Of_Table}.csv"
    try:
        with open(path_Of_Table) as file:
            csv_Reader = csv.DictReader(file)
            the_Table = [rows for rows in csv_Reader]
    except FileNotFoundError:
        pass
    return the_Table

#Write table to CSV file
def write_Table(name_Of_Table:str, table_In_List:list, table_Headers):
    path_Of_Table = f"data/{name_Of_Table}.csv"
    # if table_Headers == []:
    #     table_Headers = [header for header in table_In_List[0].keys()]
    with open(path_Of_Table, "w", newline="") as file:
        csv_Writer = csv.DictWriter(file, table_Headers)
        csv_Writer.writeheader()
        # csv_Writer.writerows(tableInList)
        for row in table_In_List:
            csv_Writer.writerow(row)

#Save database
def save_state(state):
    write_Table("couriers", state["couriers"], COURIERS_KEYS)
    write_Table("products", state["products"], PRODUCTS_KEYS)
    write_Table("orders", state["orders"], ORDERS_KEYS)
    # for each_table in state.keys():
    #     write_Table(each_table, state[each_table])

if __name__=="__main__":
    # pass
    if ui.prompt_User("Would you like to backup tables?(Y/N)\n").lower() == "y":
        write_Table("orders_backup", read_Table("orders"))
        write_Table("couriers_backup", read_Table("couriers"))
        write_Table("products_backup", read_Table("products"))