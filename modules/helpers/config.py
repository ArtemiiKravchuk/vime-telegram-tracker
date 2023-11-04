"""Helps working with config.json file"""

import sys
import json

from loguru import logger

logger = logger.opt(colors=True)


def get_data() -> any:
    """Get the whole config.json file"""
    config_path = "config.json"
    logger.debug("Retrieving info from <y>{}</>", config_path)

    try:
        with open(config_path, "r", encoding="UTF-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error("Config file <y>{}</> not found, stopping",
                     config_path)
        sys.exit(1)

    return data


def get(path: list, **kwargs) -> any:
    """Get a particular value from config.json
    For default value, `get(path, default=...)`
    (using kwargs because of implementation problems)"""
    logger.trace("Getting <y>{}</> from config", path)
    data = get_data()

    result = data
    for step in path:
        try:
            result = result[step]
        except KeyError:
            if "default" in kwargs:
                return kwargs["default"]
            else:
                logger.error("Failed to find <y>{}</> in config",
                             path)
                sys.exit(1)

    return result
