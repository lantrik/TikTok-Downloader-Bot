from asyncio import run

from bot.core import Bot, Logger


if __name__ == "__main__":
    Logger().setup()
    run(Bot().start())