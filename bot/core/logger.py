# SPDX-License-Identifier: MIT

import logging

from config import Settings


class Logger:
    """
    Base logging class.
    """
    EXTERNAL_LOGS = ("aiogram", "dispatcher.py", "http", "client", "gateway", "base_events",)
    LOG_LEVEL = logging.DEBUG if Settings.debug else logging.INFO

    LOG_FORMAT = ("{asctime} | {lineno:^3} | {filename:^16} | "
                  "{levelname:^8} | {message}")

    def __init__(self) -> None:
        self.log = logging.getLogger()

    def _stream_handler(self) -> logging.StreamHandler:
        """Returns the main logger for the console."""
        formatter = logging.Formatter(self.LOG_FORMAT, style="{")

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        return handler

    def _file_handler(self) -> logging.FileHandler:
        """Returns the logger for the file."""
        formatter = logging.Formatter(self.LOG_FORMAT, style="{")

        handler = logging.FileHandler("bot.log", encoding="utf8")
        handler.setFormatter(formatter)

        return handler
    
    def _disable_logs(self) -> None:
        """Disables extraneous loggers."""
        level = logging.DEBUG if Settings.debug else logging.CRITICAL
        for log in self.EXTERNAL_LOGS:
            logging.getLogger(log).setLevel(level)
    
    def setup(self) -> None:
        """Installing and configuring registrars."""
        self.log.setLevel(self.LOG_LEVEL)
        self._disable_logs()
        
        self.log.addHandler(self._stream_handler())
        self.log.addHandler(self._file_handler())