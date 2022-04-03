from aiogram import types
from handlers.template import template
from aiogram.dispatcher import FSMContext


async def search_year(message: types.Message, state: FSMContext):
    await template('year', message, state)
