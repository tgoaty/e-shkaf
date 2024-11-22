from aiogram import Router, F
from aiogram.types import Message
from keyboards import profile_menu

last_name = 'Иванов'
name = 'Иван'
manager = 'Менеджер'
company_title = 'Название организации'
num_orders = 123
sum_orders = 1234
discount = 5

profile_router = Router()


@profile_router.message(F.text == 'Профиль')
async def cmd_start_3(message: Message):
    await message.answer(f'''{last_name} {name}
Менеджер: {manager}
Организация: {company_title}
Заказы в работе: {num_orders}
Сумма заказов: {sum_orders}
Ваша скидка: {discount}%''', 
    reply_markup=profile_menu())
