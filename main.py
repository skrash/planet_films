from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import bot_token
from handlers.genre_state import genre_search
from handlers.search import search
from handlers.actor_search import actor_search
from handlers.author_state import author_search
from handlers.search_from_year import search_year
from handlers.affix_state import affix_state
from go_to import *
from aiogram.dispatcher import FSMContext
import sqlite3


bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def start(message: types.Message):
    # con = sqlite3.connect('db.sqlite3')
    # with con:
    #     cur = con.cursor()
    #     cur.execute('CREATE TABLE IF NOT EXIT')
    kb = back_keyboard()
    await message.answer('Напишите название фильма (можно слово) и мы найдем его для Вас!', reply_markup=kb)
    await Step.search_state.set()


async def mode(message: types.Message, state: FSMContext):
    list_mode = ['title', 'genres', 'author', 'year', 'actors']
    for i in list_mode:
        async with state.proxy() as data:
            if i in data.keys():
                del data[i]
    if message.text == 'Общий поиск':
        await go_to_search(message)
    elif message.text == 'Поиск по году':
        await go_to_search_year(message)
    elif message.text == 'Случайный фильм':
        await go_to_random(message)
    elif message.text == 'Поиск по жанру':
        await go_to_genre(message)
    elif message.text == 'Поиск по режиссёру':
        await go_to_author(message)
    elif message.text == 'По актёру':
        await go_to_actor(message)
    else:
        await message.answer('Неверная команда. Выберите подходящий поиск из предложенных ниже.')


if __name__ == '__main__':
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXIT')
    dp.register_message_handler(affix_state, state=Step.add_affix)
    dp.register_message_handler(genre_search, state=Step.genre_state)
    dp.register_message_handler(mode, state=Step.main_state)
    dp.register_message_handler(author_search, state=Step.author_state)
    dp.register_message_handler(actor_search, state=Step.actor_state)
    dp.register_message_handler(search, state=Step.search_state)
    dp.register_message_handler(search_year, state=Step.search_from_year_state)
    dp.register_message_handler(start, commands='start')
    executor.start_polling(dispatcher=dp, skip_updates=True)
