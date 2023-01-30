# SPDX-License-Identifier: MIT

from logging import getLogger
from typing import Any, List
from os import listdir
from os.path import isfile
from pathlib import Path
from importlib import import_module

from aiogram import (
    Dispatcher,
    Bot as AIOBot
)

from bot import __version__
from config import Settings, Privacy



log = getLogger()

class Bot(AIOBot):
    """
    Bot class.

    Raises
    ------
    TokenValidationError
        When token has invalid format this exception will be raised.

    Parameters
    ----------
    token: :class:`str`
        Telegram Bot token `Obtained from @BotFather <https://t.me/BotFather>`.
    """
    def __init__(self, token: str = Privacy.bot, **kwargs: Any) -> None:
        super().__init__(token, **kwargs)

        self.dp: Dispatcher = Dispatcher()

    def include_routers(self, directories: List[str] = Settings.directories) -> None:
        """
        Attach all routers.

        Parameters
        ----------
        directories: List[:class:`str`]
            Directory where routers are located
        """
        for directory in directories:
            if directory.endswith("*"):
                directory = directory.replace("*", "")

                for element in listdir(directory):
                    if element.startswith("_"):
                        continue
                    path = Path(directory, element)

                    if isfile(path):
                        path = path.as_posix().replace("/", ".")[:-3]

                        try:
                            handler = import_module(path)
                            self.dp.include_router(handler.router)

                            log.info(f"router {handler.__name__} is loaded.")
                        except Exception as exp:
                            log.exception(exp)
                            continue
            else:
                path = directory.replace("/", ".")[:-3]

                try:
                    handler = import_module(path)
                    self.dp.include_router(handler.router)

                    log.info(f"router {handler.__name__} is loaded.")
                except Exception as exp:
                    log.exception(exp)
                    continue                  

    async def start(self, **kwargs) -> None:
        """
        Bot starting.
        """
        log.info("Connecting a bot...")

        self.include_routers(**kwargs)

        await self.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self)