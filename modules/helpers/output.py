"""Save any record according to given method"""

from loguru import logger

import modules.helpers.database as db

logger = logger.opt(colors=True)


async def save_record(module: str, config: list, headers: dict,
                      data: list) -> None:
    """Save a record, according to config"""
    logger.debug("Saving a record for module <y>{}</>, data=<w>{}</>",
                 module, data)

    for output in config:
        logger.trace("Saving to output=<w>{}</>", output)
        _type = output["type"]
        name = output["name"]

        if _type == "sqlite":
            await db.save_record(name, module, headers, data)
