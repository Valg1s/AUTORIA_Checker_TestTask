import cloudscraper
import requests
from bs4 import BeautifulSoup

from sweter.telegram_bot import send_info_about_car, change_message
from sweter.models import CarInfo, session

AUTORIA_SEARCH_URL = "https://auto.ria.com/search/"
BID_URL = "https://carsbidshistory.com"

# https://auto.ria.com/search/?indexName=order_auto&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&
# country.import.usa.not=-1&country.import.id=840&abroad.not=1&custom.not=-1


def find_cars_on_autoria():
    html = requests.get(AUTORIA_SEARCH_URL, params={
        "indexName": "order_auto",
        "categories.main.id": 1,
        "brand.id[0]": 79,
        "model.id[0]": 2104,
        "country.import.usa.not": -1,
        "country.import.id": 840,
        "abroad.not": 1,
        "custom.not": -1,
    }).text

    soup = BeautifulSoup(html, "html.parser")

    search_result = soup.find("div", {"id": "searchResults"})

    items = search_result.find_all("section", {"class": "ticket-item"})

    data = []

    for item in items:
        link = item.find("a", {"class": "address"})

        car_info = item.find("ul").find_all("li")
        car_info[1].find("span").decompose()

        vin_code = item.find("div", {"class": "base_information"}).find("span", {"class": "vin-code"})

        price_block = item.find("div", {"class": "price-ticket"})
        price_usd, price_uah = price_block.find_all("span", {"data-currency": True} )

        new_data = {
            "link": link['href'],
            "car_name": link.text.strip(),
            "announce_id": item["data-advertisement-id"],
            "car_price_usd": price_usd.text.strip(),
            "car_price_uah": price_uah.text.strip(),
            "car_race": car_info[0].text.strip(),
            "car_location": car_info[1].text.strip(),
            "vin_code": vin_code.text.strip(),
        }

        data.append(new_data)

    return data


def find_link_on_auction(vin_code: str) -> str:
    """
    Get vin code of car, and find link on bidfax.info. Return link on car
    :param vin_code: string, id of car
    :return: string link on announce on bidfax.info
    """

    scraper = cloudscraper.create_scraper()

    html = scraper.get(BID_URL + f"/findbyvin/{vin_code}").text

    soup = BeautifulSoup(html, "html.parser")

    search_info = soup.find("table", {"id": "resultTable"})

    link = search_info.find("a", href=True)["href"]

    return BID_URL + link


def get_photo_from_autoria(link):
    html = requests.get(link).text

    soup = BeautifulSoup(html, "html.parser")

    pictures_box = soup.find("div", {"id": "photosBlock"}).find("div", {"class": "wrapper"})

    pictures = pictures_box.find_all("img", src=True)[:6]

    result = []

    for picture in pictures:
        result.append(picture["src"])

    return result


def get_photo_from_bid(link):
    html = requests.get(link).text

    soup = BeautifulSoup(html, "html.parser")

    pictures = soup.find("div", {"id": "slider-thumbs0"}).find_all("img", src=True)[:10]

    result = []

    for picture in pictures:
        result.append(picture["src"])

    return result


async def run_searcher():
    found_cars = find_cars_on_autoria()

    counter = 0
    for car_info in found_cars * 2:
        car = session.query(CarInfo).filter_by(announce_id=car_info['announce_id']).first()
        if car:
            if counter == 1:
                car_info['car_price_usd'] = "6500"
                car_info['car_price_uah'] = "260 000"
            result = car.update(car_info)

            session.commit()

            if result:
                await change_message(car)

            counter += 1
            continue

        bid_link = find_link_on_auction(car_info["vin_code"])

        car_info["bid_link"] = bid_link

        autoria_images = get_photo_from_autoria(car_info['link'])
        bid_images = get_photo_from_bid(bid_link)

        new_car = CarInfo.create_from_dict(car_info)

        session.add(new_car)
        session.commit()

        await send_info_about_car(car=new_car, autoria_images=autoria_images, bid_images=bid_images)


