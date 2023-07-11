import aiohttp
import logging
import requests
from bs4 import BeautifulSoup

async def fetch_api_data(url: str) -> dict | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
    except aiohttp.ClientResponseError as ex:
        logging.error(str(ex))
    except aiohttp.ClientConnectionError as ex:
        logging.error(str(ex))

async def fetch_image_data(url: str) -> str | None:
    response = requests.get(url).content
    soup = BeautifulSoup(response, "lxml")
    image = soup.find("div", class_="market_listing_largeimage").find_next("img")["src"]
    return image

async def get_item_name(url: str) -> str | None:
    if "https://steamcommunity.com/market/listings/730" not in url:
        return None
    return url.rsplit("/")[-1]

async def get_item_price(url: str) -> dict | None:
    item_name = await get_item_name(url)
    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency=5&market_hash_name={item_name}"
    
    item_data = await fetch_api_data(url)

    if item_data is not None:
        del item_data["success"]
        return item_data
    return None

async def get_item_image(url: str) -> str | None:
    item_data = await fetch_image_data(url)
    if item_data:
        return item_data
    return None
    
if __name__ == "__main__":
    import asyncio
    
    asyncio.run(get_item_image("https://steamcommunity.com/market/listings/730/AWP%20%7C%20Hyper%20Beast%20%28Battle-Scarred%29"))