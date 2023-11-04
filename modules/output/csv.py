"""Save any record to csv table"""

import os
import csv

from loguru import logger

logger = logger.opt(colors=True)


def create_table(path: str, headers: dict) -> None:
    """Create csv table with given headers"""
    logger.trace("Csv table <w>{}</> doesn't exist, creating it",
                 path)

    columns = headers.keys()

    with open(path, "w", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)


async def save_record(folder_name: str, module_name: str,
                      headers: dict, data: list) -> None:
    """Save any record to csv table"""
    logger.trace("Saving <w>{}</> into csv table <y>{}</>",
                 data, folder_name)
    folder = f"output/{folder_name}/"
    path = f"output/{folder_name}/{module_name}.csv"

    if not os.path.exists(folder):
        logger.trace("Folder <y>{}</> doesn't exist, creating it", folder)
        os.makedirs(folder)

    if not os.path.isfile(path):
        create_table(path, headers)

    with open(path, "a", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)
