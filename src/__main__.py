import src.ui_handlers as ui
import src.core as core

while True: #Main menu loop
    ui.clear_Term()
    core.print_Main_Menu()
    user_input = core.prompt_Main_Menu()
    core.main_menu_logic(user_input)