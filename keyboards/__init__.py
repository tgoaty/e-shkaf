# Пакет с клавиатурами
from .auth import auth_menu
from .menu import main_menu
from .profile import profile_menu
from .help import help_menu
from .manager import manager_menu

__all__ = [
    "auth_menu",
    "main_menu",
    "profile_menu",
    "help_menu",
    "manager_menu"
]
