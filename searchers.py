import cloudscraper
import requests
from bs4 import BeautifulSoup

from telegram_bot import send_info_about_car

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
            "car_price_usd": price_usd.text,
            "car_price_uah": price_uah.text,
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


if __name__ == "__main__":
    found_cars = find_cars_on_autoria()

    for car in found_cars:
        bid_link = find_link_on_auction(car["vin_code"])

        car["bid_link"] = bid_link

        send_info_about_car(car)

