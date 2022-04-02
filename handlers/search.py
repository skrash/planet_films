from aiogram import types
from keyboard import *
from format_video_message import message_video
from aiogram.dispatcher import FSMContext


async def search(message: types.Message, state: FSMContext):
    list_mode = ['title', 'genres', 'author', 'year', 'actors']
    list_queries = list()
    message_l = str(message.text)
    async with state.proxy() as data:
        for mode in list_mode:
            if mode in data.keys():
                list_queries.append(mode)
                list_queries.append(data[mode])
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        if len(list_queries) == 0:
            query = cur.execute(
                "SELECT title, author, actors, url, description,alter_name, year FROM films_films WHERE lower(title) like ?",
                ('%' + message_l + '%',)).fetchall()
        elif len(list_queries) == 2:
            query = cur.execute(
                f"SELECT title, author, actors, url, description,alter_name, year FROM films_films WHERE lower(title) like ? and {list_queries[0]} like ?",
                ('%' + message_l + '%', list_queries[1])).fetchall()
        elif len(list_queries) == 4:
            query = cur.execute(
                f"SELECT title, author, actors, url, description,alter_name, year FROM films_films WHERE lower(title) like ? and {list_queries[0]} like ? and {list_queries[2]} like ?",
                ('%' + message_l + '%', list_queries[1], list_queries[3])).fetchall()
        elif len(list_queries) == 6:
            query = cur.execute(
                f"SELECT title, author, actors, url, description,alter_name, year FROM films_films WHERE lower(title) like ? and {list_queries[0]} like ? and {list_queries[2]} like ? and {list_queries[4]} like ?",
                ('%' + message_l + '%', list_queries[1], list_queries[3], list_queries[5])).fetchall()
        elif len(list_queries) == 8:
            query = cur.execute(
                f"SELECT title, author, actors, url, description,alter_name, year FROM films_films WHERE lower(title) like ? and {list_queries[0]} like ? and {list_queries[2]} like ? and {list_queries[4]} like ? and {list_queries[6]} like ?",
                ('%' + message_l + '%', list_queries[1], list_queries[3], list_queries[5], list_queries[7])).fetchall()
        if len(query) > 20:
            query = query[:20]
            await message.answer('По вашему запросу найдено больше 20 фильмов. Список фильмов был сокращен до 20. Чтобы сократить выдачу, можете добавить критерий поиска.')
        if not len(query) < 1:
            for i in query:
                await message_video(message, i)
        else:
            query = cur.execute(
                "SELECT title, author, actors, url, description,alter_name, year FROM films_films WHERE lower(alter_name) like ?",
                ('%' + message_l + '%',)).fetchall()
            if not len(query) < 1:
                for i in query:
                    await message_video(message, i)
            else:
                await message.answer("Ничего не нашлось! :(")
