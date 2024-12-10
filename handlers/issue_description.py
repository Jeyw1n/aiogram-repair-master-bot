from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.callback_answer import CallbackAnswer

issue_descr_router = Router(name=__name__)

CALLS = {'phone', 'laptop', 'computer', 'vape', 'other'}


@issue_descr_router.callback_query(F.data.in_(CALLS))
async def get_issue_descriprion(callback_query: CallbackQuery) -> None:
    await callback_query.answer('Получено.')
