from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from markups import cancel_markup


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
        reply_markup=ReplyKeyboardRemove()
    )


@issue_feedback_router.callback_query(F.data.in_(CALLS))
async def get_device_name(callback_query: CallbackQuery, state: FSMContext) -> None:
    """Button click handler from the device list inline keyboard"""
    await state.set_state(Form.device_name)
    await callback_query.message.answer(
        'Напишите название устройства, которое требует ремонта:',
        reply_markup=cancel_markup(),
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
        'Опишите проблему с вашим устройством:'
    )
