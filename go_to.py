from States import Step
from keyboard import *
import sqlite3
import random
from format_video_message import message_video


async def go_to_search(message):
    kb = back_keyboard()
    await message.answer('Напишите название фильма (можно слово) и мы найдем его для Вас!', reply_markup=kb)
    await Step.search_state.set()


async def go_to_search_year(message):
    kb = back_keyboard()
    await message.answer('Напишите год выхода фильма и мы найдем его для Вас!', reply_markup=kb)
    await Step.search_from_year_state.set()


async def go_to_random(message):
    kb = back_keyboard()
    await message.answer('Случайный фильм!', reply_markup=kb)
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        query = cur.execute('SELECT COUNT(title) from films_films').fetchone() # query[0]
        rand_id = random.randint(1, int(query[0]))
        query2 = cur.execute('SELECT title, author, actors, url, description,alter_name, year from films_films where id == ?', (rand_id, ))
        for i in query2:
            await message_video(message, i)


async def go_to_genre(message):
    kb = back_keyboard()
    await message.answer('Напишите название жанра и мы найдем фильм для Вас!', reply_markup=kb)
    await Step.genre_state.set()


async def go_to_author(message):
    kb = back_keyboard()
    await message.answer('Напишите имя автора и мы найдем фильм для Вас!', reply_markup=kb)
    await Step.genre_state.set()


async def go_to_actor(message):
    kb = back_keyboard()
    await message.answer('Напишите имя актёра и мы найдем фильм для Вас!', reply_markup=kb)
    await Step.actor_state.set()
