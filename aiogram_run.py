import asyncio
from create_bot import bot, dp
from handlers import auth_router, menu_router, order_router, orderList_router, profile_router, \
    start_router


# from work_time.time_func import send_time_msg

async def main():
    dp.include_routers(
        auth_router,
        menu_router,
        orderList_router,
        order_router,
        profile_router,
        start_router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
