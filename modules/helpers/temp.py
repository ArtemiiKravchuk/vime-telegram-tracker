"""Works with temp file to save and retrieve
previous results for modules, mainly static trackers"""

import os
import json

from loguru import logger

logger = logger.opt(colors=True)


def get_temp_file_path(module: str, id: int) -> list[str]:
    """Get path for temporary file, return dir and dir+file"""
    temp_folder = f"temp/{module}/" 
    temp_file = f"temp/{module}/id{id}" 
    logger.trace("For module <y>{}</>, id <y>{}</>: temp_file=<w>{}</>",
                 module, id, temp_file)

    return [temp_folder, temp_file]


def get_prev_results(module: str, id: str) -> any:
    """Get previous results from temp"""
    logger.trace("Getting previous results for <y>{}</>, id <y>{}</>",
                 module, id)
    path= get_temp_file_path(module, id)

    if os.path.isfile(path[1]):
        with open(path[1], "r") as file:
            prev_results = json.load(file)
        logger.trace("Previous results = <w>{}</>", prev_results)

    else:
        logger.debug("No temp file <w>{}</>", path[1])
        prev_results = None

    return prev_results


def save_results(module: str, id: str, data) -> None:
    """Save results to temp"""
    logger.debug("Saving to <y>{}</>, <y>{}</> temp: <w>{}</>",
                 module, id, data)
    path = get_temp_file_path(module, id)

    if not os.path.exists(path[0]):
       os.makedirs(path[0])

    logger.trace("Dumping temp json into the file...")
    with open(path[1], "w") as file:
        json.dump(data, file)


def append_results(module: str, id: str, data) -> None:
    """Append data to existing in temp"""
    logger.debug("Appending <w>{}</> to <y>{}</> temp, id=<y>{}</>",
                 data, module, id)
    
    prev_results = get_prev_results(module, id)

    if prev_results is None:
        logger.trace("Previous results not found, writing new")
        save_results(module, id, [data])

    else:
        prev_results.append(data)
        save_results(module, id, prev_results)


def clear_temp(module: str, id: str) -> None:
    """Clear temporary files"""
    logger.debug("Clearing temp for <y>{}</>, id <y>{}</>", module, id)
    path = get_temp_file_path(module, id)

    if not os.path.isfile(path[1]):
        logger.debug("Trying to clear non-existing temp <w>{}</>",
                     path[1])

    else:
        logger.debug("Clearing records for user <y>{}</> in temp", id)
        os.remove(path[1])
