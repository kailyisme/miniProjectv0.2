import csv
import os
from prompt_toolkit.shortcuts.prompt import PromptSession
from rich.table import Table
from rich.console import Console
from rich.style import Style
# import prompt_toolkit
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

#Rich Console Style
cStyle = Style(bgcolor= "thistle1", color="black")
#Rich Console Initializer
c = Console()

def cPrint(whatToPrint):
    c.print(whatToPrint, style=cStyle, justify="center")

def importMenu(nameOfMenu:str, title:str):
    #Importing menu from file (csv)
    menuHeaders, menuBody = readMenu(nameOfMenu)
    #Construct Rich Table of the Menu
    menu = Table(title = title)
    for header in menuHeaders:
        menu.add_column(header, justify = "center", no_wrap = True)
    for eachRow in menuBody:
        menu.add_row(*eachRow)
    return menu

def readTable(nameOfTable:str):   #takes a name of table (path of table) to read
    theTable = []
    pathOfTable = f"data/{nameOfTable}.csv"
    with open(pathOfTable) as file:
        csvReader = csv.DictReader(file)
        theTable = [rows for rows in csvReader]
    return theTable

def writeTable(nameOfTable:str, tableInList:list, tableHeaders= []):
    pathOfTable = f"data/{nameOfTable}.csv"
    if tableHeaders == []:
        tableHeaders = [header for header in tableInList[0].keys()]
    with open(pathOfTable, "w", newline="") as file:
        csvWriter = csv.DictWriter(file, tableHeaders)
        csvWriter.writeheader()
        # csvWriter.writerows(tableInList)
        for row in tableInList:
            csvWriter.writerow(row)

def readMenu(nameOfMenu:str):
    pathOfMenu = f"data/{nameOfMenu}.csv"
    with open(pathOfMenu) as file:
        csvReader = csv.reader(file)
        wholeMenu = [rows for rows in csvReader]
        menuHeaders = wholeMenu[0]
        menuBody = wholeMenu[1:]
    return menuHeaders, menuBody
        

def clearTerm():
    os.system('cls' if os.name == 'nt' else 'clear')

# def initialize_prompt_session():
#     promptSession = PromptSession()
#     return promptSession

def initialize_prompt_completer(words_expected:list):
    word_completer = WordCompleter(words_expected)
    return word_completer

def initialize_prompt_completer_for_menu(nameOfMenu:str):
    toDiscard, menuBody = readMenu(nameOfMenu)
    words_expected = [each[0] for each in menuBody]
    word_completer = WordCompleter(words_expected)
    return word_completer


def promptUser(prompt, promptText="", my_completer=WordCompleter([])):
    # userInput = promptSession.prompt(f"{promptText} >")
    userInput = prompt(f"{promptText} >", completer=my_completer, complete_while_typing=True)
    return userInput.strip()

if __name__=="__main__":
    pass
    # if promptUser("Would you like to backup tables?(Y/N)\n").lower() == "y":
    #     writeTable("orders_backup", readTable("orders"))
    #     writeTable("couriers_backup", readTable("couriers"))
    #     writeTable("products_backup", readTable("products"))