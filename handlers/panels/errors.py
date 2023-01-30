from logging import getLogger

from aiogram import Router
from aiogram.types import Message
from aiogram.types.error_event import ErrorEvent



router = Router(name="Error Handler")
log = getLogger()

@router.errors()
async def errors(event: ErrorEvent) -> None:
    log.exception(event.exception)