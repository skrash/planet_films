import sqlite3
from keyboard import create_keyboard, affix_keyboard
from States import Step
from format_video_message import message_video


async def template(query, message, state):
    list_mode = ['title', 'genres', 'author', 'year', 'actors']
    raiting_order = False
    list_queries = list()
    message_l = str(message.text)
    if message.text == 'Выход на главную':
        await Step.main_state.set()
        kb = create_keyboard()
        await message.answer('Главная', reply_markup=kb)
        return None
    if message.text == 'Добавить/удалить критерий поиска':
        cur_state = await state.get_state()
        kb = affix_keyboard(cur_state.split(':')[1])
        await message.answer('Введите один из предложенных критериев и нажмите назад.', reply_markup=kb)
        async with state.proxy() as data:
            data['prev_state'] = cur_state.split(':')[1]
        await Step.add_affix.set()
        return None
    async with state.proxy() as data:
        for mode in list_mode:
            if mode in data.keys():
                list_queries.append(mode)
                list_queries.append(data[mode])
        if 'raiting' in data.keys():
            raiting_order = True
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        if len(list_queries) == 0:
            if not raiting_order:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ?",
                    ('%' + message_l + '%',)).fetchall()
            else:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? order by raiting",
                    ('%' + message_l + '%',)).fetchall()
        elif len(list_queries) == 2:
            if not raiting_order:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ?",
                    ('%' + message_l + '%', list_queries[1])).fetchall()
            else:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ? order by raiting",
                    ('%' + message_l + '%', list_queries[1])).fetchall()
        elif len(list_queries) == 4:
            if not raiting_order:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ? and {list_queries[2]} like ?",
                    ('%' + message_l + '%', list_queries[1], list_queries[3])).fetchall()
            else:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ? and {list_queries[2]} like ? order by raiting",
                    ('%' + message_l + '%', list_queries[1], list_queries[3])).fetchall()
        elif len(list_queries) == 6:
            if not raiting_order:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ? and {list_queries[2]} like ? and {list_queries[4]} like ?",
                    ('%' + message_l + '%', list_queries[1], list_queries[3], list_queries[5])).fetchall()
            else:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ? and {list_queries[2]} like ? and {list_queries[4]} like ? order by raiting",
                    ('%' + message_l + '%', list_queries[1], list_queries[3], list_queries[5])).fetchall()
        elif len(list_queries) == 8:
            if not raiting_order:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ? and {list_queries[2]} like ? and {list_queries[4]} like ? and {list_queries[6]} like ?",
                    ('%' + message_l + '%', list_queries[1], list_queries[3], list_queries[5],
                     list_queries[7])).fetchall()
            else:
                query = cur.execute(
                    f"SELECT title, author, actors, url, description,alter_name, year, raiting FROM films_films WHERE {query} like ? and {list_queries[0]} like ? and {list_queries[2]} like ? and {list_queries[4]} like ? and {list_queries[6]} like ? order by raiting",
                    ('%' + message_l + '%', list_queries[1], list_queries[3], list_queries[5],
                     list_queries[7])).fetchall()
        if len(query) > 20:
            query = query[:20]
            await message.answer(
                'По вашему запросу найдено больше 20 фильмов. Список фильмов был сокращен до 20. Чтобы сократить выдачу, можете добавить критерий поиска.')
        if not len(query) < 1:
            for i in query:
                await message_video(message, i)
        else:
            await message.answer("Ничего не нашлось! :(")
