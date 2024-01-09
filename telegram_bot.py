import asyncio

import requests
from bs4 import BeautifulSoup
from telegram import InputMediaPhoto

from settings import bot, chat_id


def run_tg_bot(func):
    def inner(data):
        loop = asyncio.get_event_loop()

        loop.run_until_complete(func(data))

    return inner


async def get_photo_from_autoria(link):
    html = requests.get(link).text

    soup = BeautifulSoup(html, "html.parser")

    pictures_box = soup.find("div", {"id": "photosBlock"}).find("div", {"class": "wrapper"})

    pictures = pictures_box.find_all("img", src=True)[:6]

    result = []

    for picture in pictures:
        result.append(picture["src"])

    return result


async def get_photo_from_bid(link):
    html = requests.get(link).text

    soup = BeautifulSoup(html, "html.parser")

    pictures = soup.find("div", {"id": "slider-thumbs0"}).find_all("img", src=True)[:4]

    result = []

    for picture in pictures:
        result.append(picture["src"])

    return result


@run_tg_bot
async def send_text(data):
    await bot.send_message(chat_id=chat_id, text=data)


@run_tg_bot
async def send_info_about_car(data):
    caption = (f"<a href='{data['link']}'>{data['car_name']}</a>\n"
               f"{data['car_price_usd']}$ / {data['car_price_uah']}₴\n"
               f"{data['car_race']}\n"
               f"{data['car_location']}\n"
               f"<a href='{data['bid_link']}'>Аукцион</a>")

    images = []

    images.extend([InputMediaPhoto(photo) for photo in await get_photo_from_autoria(data['link'])])
    images.extend([InputMediaPhoto(photo) for photo in await get_photo_from_bid(data['bid_link'])])

    await bot.send_media_group(chat_id=chat_id, caption=caption,media=images, parse_mode='html')

if __name__ == "__main__":
    send_text("Hello! It`s test task")