from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

import utils

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Вставьте ссылки предмета из стим маркета, я скажу его цену")
    
@router.message(F.text.startswith("https"))
async def proc_item(message: Message) -> None:
    item_price = await utils.get_item_price(message.text)
    item_image = await utils.get_item_image(message.text)
    del item_price["volume"]
    
    text = ""
    for key, value in item_price.items():
        text += f"{key}: {value}\n"

    text = text.replace("lowest_price", "<b>Самая низкая цена</b>")
    text = text.replace("median_price", "<b>Средняя цена</b>")
    
    await message.answer_photo(photo=item_image, caption=text)