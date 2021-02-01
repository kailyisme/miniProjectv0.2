from prompt_toolkit.shortcuts.prompt import PromptSession
import src.core as core
import datetime
from prompt_toolkit import prompt

#Initialize mainMenu
mainMenu = core.importMenu("mainMenu", "Main Menu")
def printMainMenu():
    core.cPrint(mainMenu)

#Initialize mainMenu prompt
mainMenu_options = core.initialize_prompt_completer_for_menu("mainMenu")
promp_text = "Choose/type an option:"
def prompt_mainMenu():
    userInput = core.promptUser(prompt, promp_text, mainMenu_options)
    return userInput

# #Initialize prompt session
# promptSession = core.initialize_prompt_session()

if __name__=="__main__":
    while True:
        core.clearTerm()
        printMainMenu()
        # core.promptUser(promptSession, "Choose/type an option:")
        prompt_mainMenu()