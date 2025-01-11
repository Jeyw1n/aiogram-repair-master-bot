from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from markups import (
    cancel_markup,
    main_menu_markup
)
from database import Database
from database.models import Order

issue_feedback_router = Router(name=__name__)

CALLS = {'phone', 'laptop', 'computer', 'vape', 'other'}


class Form(StatesGroup):
    device_type = State()
    device_name = State()
    description = State()


@issue_feedback_router.message(Command('cancel'))
@issue_feedback_router.message(F.text == 'Отмена ❌')
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """Allow user to cancel any action"""
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.clear()
    await message.answer(
        'Действие отменено.',
        reply_markup=main_menu_markup()
    )


@issue_feedback_router.callback_query(F.data.in_(CALLS))
async def get_device_name(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Button click handler from the device list inline keyboard"""

    # Adding device_type from the callback data
    await state.update_data(device_type=callback_query.data)
    
    await callback_query.message.edit_text(
        '*Принято!*\n' \
        'Пожалуйста, заполните форму:',
        reply_markup=None
    )
    await callback_query.answer()
    
    await state.set_state(Form.device_name)
    await callback_query.message.answer(
        'Напишите название устройства, которое требует ремонта:',
        reply_markup=cancel_markup()
    )


@issue_feedback_router.message(Form.device_name)
async def get_description(message: Message, state: FSMContext) -> None:
    """
    Writing the device name to the state machine,
    requesting a description of the problem.
    """
    # Saving device_name
    await state.update_data(device_name=message.text)
    # Setting a new state for the description
    await state.set_state(Form.description)
    await message.answer(
        'Опишите проблему с вашим устройством:',
        reply_markup=cancel_markup()
    )


DEVICES_TEXTS = {
    'phone': 'Телефон',
    'laptop': 'Ноутбук',
    'computer': 'Компютер',
    'vape': 'Вейп',
    'other': 'Другое'
}


def save_order_to_database(data: dict, user_id: int) -> None:
    try:
        conn = Database()
        
        device_type = DEVICES_TEXTS[data['device_type']]
        device_name = data['device_name']
        description = data['description']

        order = Order(user_id, device_type, device_name, description)
        conn.add_order(order)
        conn.close()
    
    except Exception as ex:
        print(f'Error when adding an order: {ex}')


@issue_feedback_router.message(Form.description)
async def final_state(message: Message, state: FSMContext) -> None:
    data = await state.update_data(description=message.text)
    await state.clear()

    description = data['description']
    device_name = data['device_name']

    # Check for exceeding the total number of characters
    if len(device_name) + len(description) > 1000:
        await message.answer(
            'Слишком много символов в названии или описании устройства. '
            'Общее количество символов не должно превышать 1000.',
            reply_markup=main_menu_markup()
        )
        return  # Exit the function if exceeded
    
    save_order_to_database(data=data, user_id=message.from_user.id)

    await message.answer(
        f'*Тип устройства:* {DEVICES_TEXTS[data["device_type"]]}\n' \
        f'*Название:* {data["device_name"]}\n' \
        f'*Описание:* {data['description']}\n\n' \
        'Ваша заявка успешно отправлена на рассмотрение. Пожалуйста, ожидайте!',
        reply_markup=main_menu_markup()
    )
