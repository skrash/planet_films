

async def message_video(message, query):
    result = ''
    result += f'Название: {query[0]}\n'
    result += f'Автор: {query[1]}\n'
    result += f'В ролях: {query[2]}\n'
    result += f'Ссылка: {query[3]}\n'
    result += f'{query[4]}\n'
    result += f'Альтернативное название: {query[5]}\n'
    result += f'Год выхода: {query[6]}\n'
    await message.reply(result)
