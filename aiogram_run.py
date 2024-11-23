import asyncio
from create_bot import bot, dp
from handlers import (
    auth_router, order_router, orderList_router, profile_router,
    start_router, manager_router, help_router
)
from logger_config import get_logger

logger = get_logger(__name__)

async def main():
    try:
        dp.include_routers(
            auth_router,
            orderList_router,
            order_router,
            profile_router,
            start_router,
            help_router,
            manager_router
        )

        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook удален, начат polling")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Произошла ошибка в процессе запуска бота: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        logger.info("Запуск бота...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Завершение программы пользователем")
    except Exception as e:
        logger.error(f"Произошла непредвиденная ошибка: {e}", exc_info=True)
