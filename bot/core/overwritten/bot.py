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
    def __init__(self, token: str = Privacy.bot, **kwargs: Any) -> None:
        super().__init__(token, **kwargs)

        self.dp: Dispatcher = Dispatcher()

    def include_routers(self, directories: List[str] = Settings.directories) -> None:
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

                            log.info(f"Модуль {handler.__name__} загружен.")
                        except Exception as exp:
                            log.exception(exp)
                            continue
            else:
                path = directory.replace("/", ".")[:-3]

                try:
                    handler = import_module(path)
                    self.dp.include_router(handler.router)

                    log.info(f"Модуль {handler.__name__} загружен.")
                except Exception as exp:
                    log.exception(exp)
                    continue                  

    async def start(self, *args, **kwargs) -> None:
        """
        Bot starting.
        """
        log.info("Connecting a bot...")

        self.include_routers(*args, **kwargs)

        await self.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self)