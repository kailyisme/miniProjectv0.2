import src.core as core
import datetime


mainMenu = core.importMenu("mainMenu", "Main Menu")
if __name__=="__main__":
    while True:
        core.clearTerm()
        mainMenu.printMenu()