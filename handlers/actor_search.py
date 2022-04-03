from aiogram import types
from handlers.template import template
from aiogram.dispatcher import FSMContext


async def actor_search(message: types.Message, state: FSMContext):
    await template('actors', message, state)
