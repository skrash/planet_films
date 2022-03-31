from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def create_keyboard():
    kb = ReplyKeyboardMarkup()
    button_search_random = KeyboardButton('Случайный фильм')
    button_main_search = KeyboardButton('Общий поиск')
    button_search_from_genre = KeyboardButton('Поиск по жанру')
    button_search_from_by = KeyboardButton('Поиск по режиссёру')
    button_search_from_year = KeyboardButton('Поиск по году')
    button_search_from_actor = KeyboardButton('По актёру')
    kb.add(button_main_search)
    kb.add(button_search_from_genre)
    kb.add(button_search_random)
    kb.add(button_search_from_by)
    kb.add(button_search_from_year)
    kb.add(button_search_from_actor)
    return kb


def back_keyboard():
    kb = ReplyKeyboardMarkup()
    affix_button = KeyboardButton('Добавить/удалить критерий поиска')
    cancel_button = KeyboardButton('Выход на главную')
    kb.add(cancel_button)
    kb.add(affix_button)
    return kb


def affix_keyboard(state):
    kb = ReplyKeyboardMarkup()
    title_button = KeyboardButton('Добавить критерий по названию')
    genre_button = KeyboardButton('Добавить критерий по жанру')
    by_button = KeyboardButton('Добавить критерий по режиссёру')
    year_button = KeyboardButton('Добавить критерий по году')
    actor_button = KeyboardButton('Добавить критерий по актёру')
    del_title_button = KeyboardButton('Удалить критерий по названию')
    del_genre_button = KeyboardButton('Удалить критерий по жанру')
    del_by_button = KeyboardButton('Удалить критерий по режиссёру')
    del_year_button = KeyboardButton('Удалить критерий по году')
    del_actor_button = KeyboardButton('Удалить критерий по актёру')
    back_button = KeyboardButton('Назад')
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
