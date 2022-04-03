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
from keyboard import *
from aiogram.dispatcher import FSMContext
import sqlite3


bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def start_recomendation(message: types.Message):
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        top3 = cur.execute('SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films where year = 2022 order by likes limit 3').fetchall()
    for i in top3:
        await message_video(message, i)


async def commands_list(message: types.Message, state: FSMContext):
    state_str = await state.get_state()
    if state_str is None:
        kb = create_keyboard()
        await message.answer('Главная', reply_markup=kb)
    else:
        state_str = state_str.split(':')[1]
        if state_str == 'main_state':
            kb = create_keyboard()
            await message.answer('Главная', reply_markup=kb)
        elif state_str == 'search_state':
            kb = back_keyboard()
            await message.answer('Напишите название фильма (можно слово) и мы найдем его для Вас!', reply_markup=kb)
        elif state_str == 'search_from_year_state':
            kb = back_keyboard()
            await message.answer('Напишите год выхода фильма и мы найдем его для Вас!', reply_markup=kb)
        elif state_str == 'add_affix':
            kb = affix_keyboard(state_str)
            await message.answer('Введите один из предложенных критериев и нажмите назад.', reply_markup=kb)
        elif state_str == 'genre_state':
            kb = back_keyboard()
            await message.answer('Напишите название жанра и мы найдем фильм для Вас!', reply_markup=kb)
        elif state_str == 'author_state':
            kb = back_keyboard()
            await message.answer('Напишите имя автора и мы найдем фильм для Вас!', reply_markup=kb)
        elif state_str == 'actor_state':
            kb = back_keyboard()
            await message.answer('Напишите имя актёра и мы найдем фильм для Вас!', reply_markup=kb)
        elif state_str == 'feedback_state':
            kb = InlineKeyboardMarkup()
            button_back = InlineKeyboardButton('Назад', go_to_main)
            kb.add(button_back)
            await message.answer('Введите сообщение для разработчика бота.', reply_markup=kb)
        elif state_str == 'for_ban_state':
            kb = InlineKeyboardMarkup()
            button_back = InlineKeyboardButton('Назад', go_to_main)
            kb.add(button_back)
            await message.answer('Введите id пользователя.', reply_markup=kb)


async def helper(message: types.Message):
    await message.answer('Список доступных команд: \n /start \n /keyboard\n')


async def feedback_msg(message: types.Message):
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        result = cur.execute('SELECT banned from users where tg_id = ?', (message.from_user.id, )).fetchone()
    if int(result[0]) == 0:
        await bot.send_message(871563164, message.text + '\n От id пользователя: ' + str(message.from_user.id))
    elif int(result[0]) == 1:
        await message.answer('Разработчик вас заблокировал.')


async def for_ban(callback_query: CallbackQuery):
    kb = InlineKeyboardMarkup()
    button_back = InlineKeyboardButton('Назад', callback_data='go_to_main')
    kb.add(button_back)
    await callback_query.message.answer('Введите id пользователя.', reply_markup=kb)
    await Step.for_ban_state.set()


async def start(message: types.Message):
    await start_recomendation(message)
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        user = cur.execute(f'SELECT id from users where tg_id == {message.chat.id}').fetchone()
    con2 = sqlite3.connect('db.sqlite3')
    if user is None:
        with con2:
            cur2 = con2.cursor()
            cur2.execute(f'INSERT INTO users VALUES (NULL, {message.chat.id}, 0)')
            con2.commit()
    if message.from_user.id == 871563164:
        kb = create_keyboard_admin()
    else:
        kb = create_keyboard()
    await message.answer('Главная', reply_markup=kb)
    await Step.main_state.set()


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


async def who_ban(message: types.Message):
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        cur.execute('UPDATE users SET banned = 1 where tg_id = ?', (int(message.text), ))
        con.commit()
    await message.answer('SUCCESS!')


if __name__ == '__main__':
    dp.register_callback_query_handler(feedback, text='feedback', state='*')
    dp.register_message_handler(feedback_msg, state=Step.feedback_state)
    dp.register_callback_query_handler(for_ban, text='ban', state='*')
    dp.register_message_handler(who_ban, state=Step.for_ban_state)

    dp.register_message_handler(helper, commands='help', state='*')
    dp.register_message_handler(commands_list, commands='keyboard', state='*')
    dp.register_callback_query_handler(go_to_random, text='random_films', state='*')
    dp.register_callback_query_handler(go_to_search, text='main_search', state='*')
    dp.register_callback_query_handler(go_to_genre, text='search_from_genre', state='*')
    dp.register_callback_query_handler(go_to_author, text='search_from_author', state='*')
    dp.register_callback_query_handler(go_to_search_year, text='search_from_year', state='*')
    dp.register_callback_query_handler(go_to_actor, text='search_from_actor', state='*')

    dp.register_callback_query_handler(go_to_main, text='go_to_main', state='*')
    dp.register_callback_query_handler(go_to_add_affix, text='go_to_affix', state='*')

    dp.register_callback_query_handler(affix_title, text='affix_title', state='*')
    dp.register_callback_query_handler(affix_genre, text='affix_genre', state='*')
    dp.register_callback_query_handler(affix_author, text='affix_author', state='*')
    dp.register_callback_query_handler(affix_year, text='affix_year', state='*')
    dp.register_callback_query_handler(affix_actor, text='affix_actors', state='*')
    dp.register_callback_query_handler(del_affix_title, text='del_affix_title', state='*')
    dp.register_callback_query_handler(del_affix_genres, text='del_affix_genre', state='*')
    dp.register_callback_query_handler(del_affix_author, text='del_affix_author', state='*')
    dp.register_callback_query_handler(del_affix_year, text='del_affix_year', state='*')
    dp.register_callback_query_handler(del_affix_actors, text='del_affix_actors', state='*')
    dp.register_callback_query_handler(back_on_affix, text='back_on_affix', state='*')
    dp.register_callback_query_handler(affix_raiting, text='affix_raiting', state='*')
    dp.register_callback_query_handler(del_affix_raiting, text='del_affix_raiting', state='*')

    dp.register_callback_query_handler(user_like_vote, text='like', state='*')
    dp.register_callback_query_handler(user_dislike_vote, text='dislike', state='*')
    dp.register_message_handler(affix_state, state=Step.add_affix)
    dp.register_message_handler(genre_search, state=Step.genre_state)
    dp.register_message_handler(mode, state=Step.main_state)
    dp.register_message_handler(author_search, state=Step.author_state)
    dp.register_message_handler(actor_search, state=Step.actor_state)
    dp.register_message_handler(search, state=Step.search_state)
    dp.register_message_handler(search_year, state=Step.search_from_year_state)
    dp.register_message_handler(start, commands='start')
    executor.start_polling(dispatcher=dp, skip_updates=True)
