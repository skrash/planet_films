from aiogram import types
from handlers.template import template


async def actor_search(message: types.Message):
    await template('actors', message)
