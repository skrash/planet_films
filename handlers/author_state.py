from aiogram import types
from handlers.template import template


async def author_search(message: types.Message):
    await template('author', message)
