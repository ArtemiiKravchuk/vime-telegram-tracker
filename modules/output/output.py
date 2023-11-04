"""Save any record according to given method"""

from loguru import logger

import modules.output.database as db
import modules.helpers.config as cn
import modules.output.csv as cs

logger = logger.opt(colors=True)


async def save_record(module: str, headers: dict, data: list) -> None:
    """Save a record, according to config"""
    logger.debug("Saving a record for module <y>{}</>, data=<w>{}</>",
                 module, data)

    for output in cn.get(["output"]):
        logger.trace("Saving to output=<w>{}</>", output)
        _type = output["type"]
        name = output["name"]

        if _type == "sqlite":
            await db.save_record(name, module, headers, data)

        elif _type == "csv":
            await cs.save_record(name, module, headers, data)
