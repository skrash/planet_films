from aiogram import types
from aiogram.dispatcher import FSMContext


async def affix_state(message: types.Message, state: FSMContext):
    list_mode = ['title', 'genres', 'author', 'year', 'actors']
    async with state.proxy() as data:
        if data['mode'] != '':
            if data['mode'] in list_mode:
                async with state.proxy() as data2:
                    data2[data['mode']] = message.text
                    await message.answer('Критерий добавлен!')
        else:
            await message.answer('Сначала необходимо выбрать критерий для поиска!')
