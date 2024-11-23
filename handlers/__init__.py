# Пакет с обработчиками сообщений
from .auth import auth_router
from .profile import profile_router
from .order import order_router
from .orderList import orderList_router
from .start import start_router
from .help import help_router
from .manager import manager_router


__all__ = [
    "auth_router",
    "profile_router",
    "order_router",
    "orderList_router",
    "start_router",
    "help_router",
    "manager_router"
]
