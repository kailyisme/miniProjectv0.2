import csv
import src.ui_handlers as ui

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

if __name__=="__main__":
    # pass
    if ui.prompt_User("Would you like to backup tables?(Y/N)\n").lower() == "y":
        write_Table("orders_backup", read_Table("orders"))
        write_Table("couriers_backup", read_Table("couriers"))
        write_Table("products_backup", read_Table("products"))