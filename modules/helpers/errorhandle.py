"""Helps with handling exceptions in asyncio tasks"""

from loguru import logger

logger = logger.opt(colors=True)


async def log(awaitable) -> any:
    """Log exceptions in asyncio task"""

    try:
        return await awaitable
    except Exception as e:
        logger.exception(e)
