import asyncio

from telegram import InputMediaPhoto

from sweter import chat_id,bot
from sweter.models import CarInfo,session


def run_tg_bot(func):

    async def inner(data, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(func(data, kwargs))
        loop.close()

    return inner


@run_tg_bot
async def send_text(data):
    await bot.send_message(chat_id=chat_id, text=data)


async def change_message(car: CarInfo):

    caption = (f"<a href='{car.link}'>{car.car_name}</a>\n"
               f"{car.car_price_usd}$ / {car.car_price_uah}₴\n"
               f"{car.car_race}\n"
               f"{car.car_location}\n"
               f"<a href='{car.bid_link}'>Аукцион</a>")

    try:
        await bot.editMessageCaption(chat_id=chat_id, message_id=car.message_id, caption=caption, parse_mode='html')

        await bot.send_message(chat_id=chat_id, reply_to_message_id=car.message_id, text="Внимание! Цена была изменена.")
    except Exception as e:
        print("Error excepted and ignored", e)


async def send_info_about_car(car: CarInfo, **kwargs):
    caption = (f"<a href='{car.link}'>{car.car_name}</a>\n"
               f"{car.car_price_usd}$ / {car.car_price_uah}₴\n"
               f"{car.car_race}\n"
               f"{car.car_location}\n"
               f"<a href='{car.bid_link}'>Аукцион</a>")

    images = []
    bid_images = []

    images.extend([InputMediaPhoto(photo) for photo in kwargs['autoria_images']])
    bid_images.extend([InputMediaPhoto(photo) for photo in kwargs['bid_images']])

    try:
        messages = await bot.send_media_group(chat_id=chat_id, caption=caption,media=images, parse_mode='html')

        message_id = messages[0].message_id

        car.message_id = message_id
        session.commit()

        await bot.send_media_group(chat_id=chat_id, caption="Фото с аукциона", media=bid_images)
    except Exception as e:
        print("Error excepted and ignored", e)


if __name__ == "__main__":
    send_text("Hello! It`s test task")