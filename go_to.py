from States import Step
from keyboard import *
import sqlite3
import random
from format_video_message import message_video
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext


async def go_to_main(callback_query: CallbackQuery):
    await Step.main_state.set()
    kb = create_keyboard()
    await callback_query.message.answer('Главная', reply_markup=kb)
    return None


async def go_to_add_affix(callback_query: CallbackQuery, state: FSMContext):
    cur_state = await state.get_state()
    kb = affix_keyboard(cur_state.split(':')[1])
    await callback_query.message.answer('Введите один из предложенных критериев и нажмите назад.', reply_markup=kb)
    async with state.proxy() as data:
        data['prev_state'] = cur_state.split(':')[1]
    await Step.add_affix.set()
    return None


async def go_to_search(callback_query: CallbackQuery):
    kb = back_keyboard()
    await callback_query.message.answer('Напишите название фильма (можно слово) и мы найдем его для Вас!', reply_markup=kb)
    await Step.search_state.set()


async def go_to_search_year(callback_query: CallbackQuery):
    kb = back_keyboard()
    await callback_query.message.answer('Напишите год выхода фильма и мы найдем его для Вас!', reply_markup=kb)
    await Step.search_from_year_state.set()


async def go_to_random(callback_query: CallbackQuery):
    kb = back_keyboard()
    await callback_query.message.answer('Случайный фильм!', reply_markup=kb)
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        query = cur.execute('SELECT COUNT(title) from films_films').fetchone() # query[0]
        rand_id = random.randint(1, int(query[0]))
        query2 = cur.execute('SELECT title, author, actors, url, description,alter_name, year from films_films where id == ?', (rand_id, ))
        for i in query2:
            await message_video(callback_query.message, i)


async def go_to_genre(callback_query: CallbackQuery):
    kb = back_keyboard()
    await callback_query.message.answer('Напишите название жанра и мы найдем фильм для Вас!', reply_markup=kb)
    await Step.genre_state.set()


async def go_to_author(callback_query: CallbackQuery):
    kb = back_keyboard()
    await callback_query.message.answer('Напишите имя автора и мы найдем фильм для Вас!', reply_markup=kb)
    await Step.genre_state.set()


async def go_to_actor(callback_query: CallbackQuery):
    kb = back_keyboard()
    await callback_query.message.answer('Напишите имя актёра и мы найдем фильм для Вас!', reply_markup=kb)
    await Step.actor_state.set()


async def affix_title(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = 'title'
    await callback_query.message.answer('Введите слово или его часть из названия фильма.')


async def affix_genre(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = 'genres'
    await callback_query.message.answer('Введите название жанра.')


async def affix_author(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = 'author'
    await callback_query.message.answer('Введите имя режиссёра.')


async def affix_year(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = 'year'
    await callback_query.message.answer('Введите год выхода фильма.')


async def affix_actor(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['mode'] = 'actors'
    await callback_query.message.answer('Введите имя актёра.')


async def del_affix_title(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        del data['title']


async def del_affix_genres(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        del data['genres']


async def del_affix_author(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        del data['author']


async def del_affix_year(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        del data['year']


async def del_affix_actors(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        del data['actors']


async def affix_raiting(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['raiting'] = ''
    await callback_query.message.answer('Готово!')


async def del_affix_raiting(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        del data['raiting']


async def back_on_affix(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['prev_state'] == 'search_state':
            await go_to_search(callback_query)
        elif data['prev_state'] == 'search_from_year_state':
            await go_to_search_year(callback_query)
        elif data['prev_state'] == 'genre_state':
            await go_to_genre(callback_query)
        elif data['prev_state'] == 'author_state':
            await go_to_author(callback_query)
        elif data['prev_state'] == 'actor_state':
            await go_to_actor(callback_query)


async def feedback(callback_query: CallbackQuery):
    kb = InlineKeyboardMarkup()
    button_back = InlineKeyboardButton('Назад', callback_data='go_to_main')
    kb.add(button_back)
    await callback_query.message.answer('Введите сообщение для разработчика бота.', reply_markup=kb)
    await Step.feedback_state.set()
