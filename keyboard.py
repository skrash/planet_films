# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery
import re
import sqlite3


def create_keyboard():
    kb = InlineKeyboardMarkup()
    button_search_random = InlineKeyboardButton('Случайный фильм', callback_data='random_films')
    button_main_search = InlineKeyboardButton('Общий поиск', callback_data='main_search')
    button_search_from_genre = InlineKeyboardButton('Поиск по жанру', callback_data='search_from_genre')
    button_search_from_by = InlineKeyboardButton('Поиск по режиссёру', callback_data='search_from_author')
    button_search_from_year = InlineKeyboardButton('Поиск по году', callback_data='search_from_year')
    button_search_from_actor = InlineKeyboardButton('По актёру', callback_data='search_from_actor')
    button_feedback = InlineKeyboardButton('Отправить сообщение разработчику', callback_data='feedback')
    kb.add(button_main_search)
    kb.add(button_search_from_genre)
    kb.add(button_search_random)
    kb.add(button_search_from_by)
    kb.add(button_search_from_year)
    kb.add(button_search_from_actor)
    kb.add(button_feedback)
    return kb


def create_keyboard_admin():
    kb = InlineKeyboardMarkup()
    affix_button = InlineKeyboardButton('Добавить/удалить критерий поиска', callback_data='go_to_affix')
    cancel_button = InlineKeyboardButton('Выход на главную', callback_data='go_to_main')
    button_ban = InlineKeyboardButton('Заблокировать', callback_data='ban')
    kb.add(cancel_button)
    kb.add(affix_button)
    kb.add(button_ban)
    return kb


def back_keyboard():
    kb = InlineKeyboardMarkup()
    affix_button = InlineKeyboardButton('Добавить/удалить критерий поиска', callback_data='go_to_affix')
    cancel_button = InlineKeyboardButton('Выход на главную', callback_data='go_to_main')
    kb.add(cancel_button)
    kb.add(affix_button)
    return kb


def affix_keyboard(state):
    kb = InlineKeyboardMarkup()
    title_button = InlineKeyboardButton('Добавить критерий по названию', callback_data='affix_title')
    genre_button = InlineKeyboardButton('Добавить критерий по жанру', callback_data='affix_genre')
    by_button = InlineKeyboardButton('Добавить критерий по режиссёру', callback_data='affix_author')
    year_button = InlineKeyboardButton('Добавить критерий по году', callback_data='affix_year')
    actor_button = InlineKeyboardButton('Добавить критерий по актёру', callback_data='affix_actors')
    del_title_button = InlineKeyboardButton('Удалить критерий по названию', callback_data='del_affix_title')
    del_genre_button = InlineKeyboardButton('Удалить критерий по жанру', callback_data='del_affix_genre')
    del_by_button = InlineKeyboardButton('Удалить критерий по режиссёру', callback_data='del_affix_author')
    del_year_button = InlineKeyboardButton('Удалить критерий по году', callback_data='del_affix_year')
    del_actor_button = InlineKeyboardButton('Удалить критерий по актёру', callback_data='del_affix_actors')
    back_button = InlineKeyboardButton('Назад', callback_data='back_on_affix')
    if state == 'search_state':
        kb.add(genre_button)
        kb.add(by_button)
        kb.add(year_button)
        kb.add(actor_button)
        kb.add(del_genre_button)
        kb.add(del_by_button)
        kb.add(del_year_button)
        kb.add(del_actor_button)
    if state == 'search_from_year_state':
        kb.add(genre_button)
        kb.add(by_button)
        kb.add(title_button)
        kb.add(actor_button)
        kb.add(del_genre_button)
        kb.add(del_by_button)
        kb.add(del_title_button)
        kb.add(del_actor_button)
    if state == 'genre_state':
        kb.add(year_button)
        kb.add(by_button)
        kb.add(title_button)
        kb.add(actor_button)
        kb.add(del_year_button)
        kb.add(del_by_button)
        kb.add(del_title_button)
        kb.add(del_actor_button)
    if state == 'author_state':
        kb.add(year_button)
        kb.add(genre_button)
        kb.add(title_button)
        kb.add(actor_button)
        kb.add(del_year_button)
        kb.add(del_genre_button)
        kb.add(del_title_button)
        kb.add(del_actor_button)
    if state == 'actor_state':
        kb.add(year_button)
        kb.add(genre_button)
        kb.add(title_button)
        kb.add(by_button)
        kb.add(del_year_button)
        kb.add(del_genre_button)
        kb.add(del_title_button)
        kb.add(del_by_button)
    kb.add(back_button)
    return kb


async def user_like_vote(callback_query: CallbackQuery):
    title = callback_query.message.text[re.search('Название: ', callback_query.message.text).end():]
    title = title[0:re.search('\n', title).start()]
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        result = cur.execute(f'SELECT who_like, who_dislike from films_films where title == ?',
                             (title,)).fetchone()
    if result[0] is None or result[1] is None:
        result8 = list()
        if result[0] is None:
            result8.append('')
        else:
            result8.append(result[0])
        if result[1] is None:
            result8.append('')
        else:
            result8.append(result[1])
        result = result8
    if str(callback_query.from_user.id) in result[1]:  # если уже дизлайкнул
        with con:
            cur = con.cursor()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                  (title,)).fetchone()
            dislike = int(result2[1]) - 1
            cur.execute('UPDATE films_films SET dislikes = ? where title = ?', (dislike, title))  # убрать дизлайк
            con.commit()
            result3 = cur.execute('SELECT who_dislike from films_films where title == ?',
                                  (title,)).fetchone()
            result4 = str(result3[0])
            result4 = result4.replace(f', {callback_query.from_user.id}', '')
            cur.execute('UPDATE films_films SET who_dislike = ? where title == ?', (result4, title))  # убрать себя из дизлайкнувших
            con.commit()
            result5 = cur.execute('SELECT who_like from films_films where title == ?',
                                  (title,)).fetchone()
            result6 = str(result5[0]) + ', ' + str(callback_query.from_user.id)
            cur.execute('UPDATE films_films SET who_like = ? where title = ?', (result6, title))  # добавить себя в лайкнувшие
            con.commit()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                  (title,)).fetchone()
            likes = int(result2[0]) + 1
            cur.execute('UPDATE films_films SET likes = ? where title = ?', (likes, title))  # добавить лайк
            con.commit()
        kb = inline_keyboard(likes, dislike)
        await callback_query.message.edit_text(callback_query.message.text, reply_markup=kb)
    elif str(callback_query.from_user.id) in result[0]:  # если уже лайкнул
        with con:
            cur = con.cursor()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                  (title,)).fetchone()
            likes = int(result2[0]) - 1
            cur.execute('UPDATE films_films SET likes = ? where title = ?', (likes, title))  # убрать лайк
            con.commit()
            result3 = cur.execute('SELECT who_like from films_films where title == ?',
                                  (title,)).fetchone()
            result4 = str(result3[0])
            result4 = result4.replace(f', {callback_query.from_user.id}', '')
            cur.execute('UPDATE films_films SET who_like = ? where title == ?', (result4, title))  # убрать себя из лайкнувших
            con.commit()
        kb = inline_keyboard(likes, result2[1])
        await callback_query.message.edit_text(callback_query.message.text, reply_markup=kb)
    else:
        with con:
            cur = con.cursor()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                  (title,)).fetchone()
            likes = int(result2[0]) + 1
            cur.execute('UPDATE films_films SET likes = ? where title = ?', (likes, title))  # добавить лайк
            con.commit()
            result5 = cur.execute(f'SELECT who_like from films_films where title == ?',
                                  (title,)).fetchone()
            result6 = str(result5[0]) + ', ' + str(callback_query.from_user.id)
            cur.execute('UPDATE films_films SET who_like = ? where title = ?', (result6, title))  # добавить себя в лайкнувшие
            con.commit()
        kb = inline_keyboard(likes, int(result2[1]))
        await callback_query.message.edit_text(callback_query.message.text, reply_markup=kb)


async def user_dislike_vote(callback_query: CallbackQuery):
    title = callback_query.message.text[re.search('Название: ', callback_query.message.text).end():]
    title = title[0:re.search('\n', title).start()]
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        result = cur.execute(f'SELECT who_like, who_dislike from films_films where title == ?',
                             (title,)).fetchone()
    if result[0] is None or result[1] is None:
        result8 = list()
        if result[0] is None:
            result8.append('')
        else:
            result8.append(result[0])
        if result[1] is None:
            result8.append('')
        else:
            result8.append(result[1])
        result = result8
    if str(callback_query.from_user.id) in result[0]:  # если уже лайкнул
        with con:
            cur = con.cursor()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                 (title,)).fetchone()
            likes = int(result2[0]) - 1
            cur.execute('UPDATE films_films SET likes = ? where title = ?', (likes, title))  # убрать лайк
            con.commit()
            result3 = cur.execute('SELECT who_like from films_films where title == ?',
                                 (title,)).fetchone()
            result4 = str(result3[0])
            result4 = result4.replace(f', {callback_query.from_user.id}', '')
            cur.execute('UPDATE films_films SET who_like = ? where title == ?', (result4, title))  # убрать себя из лайкнувших
            con.commit()
            result5 = cur.execute('SELECT who_dislike from films_films where title == ?',
                                  (title,)).fetchone()
            result6 = str(result5[0]) + ', ' + str(callback_query.from_user.id)
            cur.execute('UPDATE films_films SET who_dislike = ? where title = ?', (result6, title))  # добавить себя в дизлайкнувшие
            con.commit()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                  (title,)).fetchone()
            dislikes = int(result2[1]) + 1
            cur.execute('UPDATE films_films SET dislikes = ? where title = ?', (dislikes, title))  # добавить дизлайк
            con.commit()
        kb = inline_keyboard(likes, dislikes)
        await callback_query.message.edit_text(callback_query.message.text, reply_markup=kb)
    elif str(callback_query.from_user.id) in result[1]:  # если уже дизлайкнул
        with con:
            cur = con.cursor()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                  (title,)).fetchone()
            likes = int(result2[1]) - 1
            cur.execute('UPDATE films_films SET dislikes = ? where title = ?', (likes, title))  # убрать дизлайк
            con.commit()
            result3 = cur.execute('SELECT who_dislike from films_films where title == ?',
                                  (title,)).fetchone()
            result4 = str(result3[0])
            result4 = result4.replace(f', {callback_query.from_user.id}', '')
            cur.execute('UPDATE films_films SET who_dislike = ?  where title == ?', (result4, title))  # убрать себя из дизлайкнувших
            con.commit()
        kb = inline_keyboard(result2[0], likes)
        await callback_query.message.edit_text(callback_query.message.text, reply_markup=kb)
    else:
        with con:
            cur = con.cursor()
            result2 = cur.execute('SELECT likes, dislikes from films_films where title == ?',
                                  (title,)).fetchone()
            likes = int(result2[1]) + 1
            cur.execute('UPDATE films_films SET dislikes = ? where title = ?', (likes, title))  # добавить дизлайк
            con.commit()
            result5 = cur.execute(f'SELECT who_dislike from films_films where title == ?',
                                  (title,)).fetchone()
            result6 = str(result5[0]) + ', ' + str(callback_query.from_user.id)
            cur.execute('UPDATE films_films SET who_dislike = ? where title == ?', (result6, title))  # добавить себя в дизлайкнувшие
            con.commit()
        kb = inline_keyboard(int(result2[0]), likes)
        await callback_query.message.edit_text(callback_query.message.text, reply_markup=kb)


def inline_keyboard(likes, dislikes):
    kb = InlineKeyboardMarkup()
    button_like = InlineKeyboardButton(u'\U0001F44D' + f' ({likes})', callback_data='like')
    button_dislike = InlineKeyboardButton(u'\U0001F44E' + f' ({dislikes})', callback_data='dislike')
    kb.row(button_like, button_dislike)
    return kb
