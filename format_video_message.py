import aiogram.types
from keyboard import inline_keyboard
import sqlite3


async def message_video(message: aiogram.types.Message, query):
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        result = cur.execute(f'SELECT likes, dislikes from films_films where title == ?',
                              (query[0],)).fetchone()
    kb = inline_keyboard(result[0], result[1])
    result = ''
    result += f'Название: {query[0]}\n'
    result += f'Автор: {query[1]}\n'
    result += f'В ролях: {query[2]}\n'
    result += f'Ссылка: {query[3]}\n'
    result += f'{query[4]}\n'
    result += f'Альтернативное название: {query[5]}\n'
    result += f'Год выхода: {query[6]}\n'
    await message.answer(result, reply_markup=kb)
