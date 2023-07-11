import logging
import asyncio

from aiogram import Bot, Dispatcher

import handlers
from config_reader import config

logger = logging.getLogger(__name__)

def setup_logger(level: logging) -> None:
    format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    logging.basicConfig(level=level, format=format)

async def main() -> None:
    dp = Dispatcher()
    dp.include_router(handlers.router)
    
    bot = Bot(token=config.token, parse_mode="HTML")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        
if __name__ == "__main__":
    setup_logger(logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("bot stopped by ctrl+c")