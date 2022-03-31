from aiogram import types
from aiogram.dispatcher import FSMContext
from go_to import *


async def affix_state(message: types.Message, state: FSMContext):
    list_mode = ['title', 'genres', 'author', 'year', 'actors']
    if message.text == 'Добавить критерий по названию':
        async with state.proxy() as data:
            data['mode'] = list_mode[0]
        await message.answer('Введите слово или его часть из названия фильма.')
    elif message.text == 'Добавить критерий по жанру':
        async with state.proxy() as data:
            data['mode'] = list_mode[1]
        await message.answer('Введите название жанра.')
    elif message.text == 'Добавить критерий по режиссёру':
        async with state.proxy() as data:
            data['mode'] = list_mode[2]
        await message.answer('Введите имя режиссёра.')
    elif message.text == 'Добавить критерий по году':
        async with state.proxy() as data:
            data['mode'] = list_mode[3]
        await message.answer('Введите год выхода фильма.')
    elif message.text == 'Добавить критерий по актёру':
        async with state.proxy() as data:
            data['mode'] = list_mode[4]
        await message.answer('Введите имя актёра.')
    elif message.text == 'Удалить критерий по названию':
        async with state.proxy() as data:
            del data['title']
    elif message.text == 'Удалить критерий по жанру':
        async with state.proxy() as data:
            del data['genres']
    elif message.text == 'Удалить критерий по режиссёру':
        async with state.proxy() as data:
            del data['author']
    elif message.text == 'Удалить критерий по году':
        async with state.proxy() as data:
            del data['year']
    elif message.text == 'Удалить критерий по актёру':
        async with state.proxy() as data:
            del data['actors']
    elif message.text == 'Назад':
        async with state.proxy() as data:
            if data['prev_state'] == 'search_state':
                await go_to_search(message)
            elif data['prev_state'] == 'search_from_year_state':
                await go_to_search_year(message)
            elif data['prev_state'] == 'genre_state':
                await go_to_genre(message)
            elif data['prev_state'] == 'author_state':
                await go_to_author(message)
            elif data['prev_state'] == 'actor_state':
                await go_to_actor(message)
    else:
        async with state.proxy() as data:
            if data['mode'] != '':
                if data['mode'] in list_mode:
                    async with state.proxy() as data2:
                        data2[data['mode']] = message.text
                        await message.answer('Критерий добавлен!')
            else:
                await message.answer('Сначала необходимо выбрать критерий для поиска!')
