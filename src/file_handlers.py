import csv
import src.constants as constants

# Read table from CSV file
def read_Table(name_Of_Table: str):
    the_table = []
    path_Of_Table = f"to_import/{name_Of_Table}.csv"
    try:
        with open(path_Of_Table) as file:
            csv_Reader = csv.DictReader(file)
            the_table = [rows for rows in csv_Reader]
    except FileNotFoundError:
        pass
    return the_table


# Write table to CSV file
def write_Table(name_Of_Table: str, table_in_list: list, table_Headers):
    path_Of_Table = f"data/{name_Of_Table}.csv"
    with open(path_Of_Table, "w", newline="") as file:
        csv_Writer = csv.DictWriter(file, table_Headers)
        csv_Writer.writeheader()
        # csv_Writer.writerows(tableInList)
        for row in table_in_list:
            csv_Writer.writerow(row)


# Save database
def save_state(state):
    for table_name in state.keys():
        write_Table(table_name, state[table_name], constants.get_keys(table_name))
