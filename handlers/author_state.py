from aiogram import types
from handlers.template import template
from aiogram.dispatcher import FSMContext


async def author_search(message: types.Message, state: FSMContext):
    await template('author', message, state)
