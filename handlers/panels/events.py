from logging import getLogger

from aiogram import Router

from bot import __version__



router = Router(name="General events")
log = getLogger()

@router.startup()
async def on_startup() -> None:
    """Base startup event."""
    log.info(f"Bot is ready! | Version: {__version__}")

@router.shutdown()
async def on_shutdown() -> None:
    """Base shutdown event."""
    log.info(f"Bot is shutdown.")