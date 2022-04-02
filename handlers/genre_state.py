from aiogram import types
from handlers.template import template


async def genre_search(message: types.Message):
    await template('genres', message)
