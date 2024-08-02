from aiogram_dialog import Dialog, LaunchMode

from .widgets import main_menu_window


main_menu_dialog = Dialog(
    main_menu_window,
    launch_mode=LaunchMode.ROOT
)
