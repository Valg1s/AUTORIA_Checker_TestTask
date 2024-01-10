from telegram import InputMediaPhoto

from sweter import chat_id, bot
from sweter.models import CarInfo, session


async def send_info_about_sell(car: CarInfo) -> None:
    """
    Send to channel information about selling car
    :param car: DB instance
    :return: None
    """
    try:
        await bot.send_message(chat_id=chat_id, reply_to_message_id=car.message_id, text="Автомобиль был продан!")
    except Exception as e:
        print("Error excepted and ignored in func SEndInfoAboutSell", e)


async def change_message(car: CarInfo) -> None:
    """
    Change cost and send notification about this
    :param car: DB instance
    :return: None
    """
    caption = (f"<a href='{car.link}'>{car.car_name}</a>\n"
               f"{car.car_price_usd}$ / {car.car_price_uah}₴\n"
               f"{car.car_race}\n"
               f"{car.car_location}\n"
               f"<a href='{car.bid_link}'>Аукцион</a>")

    try:
        await bot.editMessageCaption(chat_id=chat_id, message_id=car.message_id, caption=caption, parse_mode='html')

        await bot.send_message(chat_id=chat_id, reply_to_message_id=car.message_id,
                               text="Внимание! Цена была изменена.")
    except Exception as e:
        print("Error excepted and ignored in func ChangeMessage", e)


async def send_info_about_car(car: CarInfo, **kwargs) -> None:
    """
    Send information about car with photo on channel
    :param car: DB instance
    :param kwargs: links on images
    :return: None
    """
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
        messages = await bot.send_media_group(chat_id=chat_id, caption=caption, media=images, parse_mode='html')

        message_id = messages[0].message_id

        car.message_id = message_id
        session.commit()

        await bot.send_media_group(chat_id=chat_id, caption="Фото с аукциона", media=bid_images)
    except Exception as e:
        print("Error excepted and ignored in SendInfoAboutCar", e)
