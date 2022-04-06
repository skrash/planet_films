import sqlite3
from aiogram.types import Message
from aiogram.types import LabeledPrice
from aiogram.types import PreCheckoutQuery
from config import payment_token


async def donation(message: Message):
    try:
        cash = int(message.text)
    except ValueError as e:
        await message.answer('Неверно введена сумма. Введите сумму в рублях.')
    except Exception as e:
        await message.answer('Что-то пошло не так!')

    if cash < 85:
        await message.answer('Минимальная сумма 85 рублей!')
        return None

    cash_real = cash * 100
    price = LabeledPrice(label='Пожертвование', amount=cash_real)

    await message.bot.send_invoice(
        message.chat.id,
        title=f'Пожертвование',
        description=f'Пожертвование на сумму {cash} рублей',
        provider_token=payment_token,
        currency='rub',
        photo_url=None,
        photo_height=None,
        photo_width=None,
        photo_size=None,
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[price],
        start_parameter='donate',
        payload='some-invoice-payload-for-our-internal-use')


async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_successful_payment(message: Message):
    await message.bot.send_message(message.from_user.id, 'Спонсорам доступна группа с разработчиком! https://t.me/+Gi_WljQQdeVhMTIy')
    pmnt = message.successful_payment.to_python()
    con = sqlite3.connect('db.sqlite3')
    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO payment VALUES (NULL, ?, 1, ?, ?, ?)', (
        message.from_user.id, pmnt['telegram_payment_charge_id'], pmnt['provider_payment_charge_id'],
        int(pmnt['total_amount']) / 100))
        con.commit()
