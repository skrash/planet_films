from aiogram import types
from handlers.template import template


async def search_year(message: types.Message):
    await template('year', message)
