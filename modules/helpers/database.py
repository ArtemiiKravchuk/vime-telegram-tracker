"""Save any record to sqlite database"""

import os

import aiosqlite
from loguru import logger

logger = logger.opt(colors=True)


async def table_exists(cur, name: str) -> bool:
    """Check if given table by it's name exists in db"""
    logger.trace("Checking if table <y>{}</> exists", name)
    await cur.execute("SELECT count(name) FROM sqlite_master WHERE \
type='table' AND name=?", [name])

    result = await cur.fetchone()
    return result[0]==1


async def create_table(cur, module_name: str, headers: dict) -> None:
    """Create table with given headers and name. Doesn't
    check, if the table already exists"""
    logger.info("Table <y>{}</> doesn't exist, creating it",
                module_name)

    column_def = ["id INTEGER"]
    for col_name, _type in headers.items():
        logger.trace("Working with col <y>{}</>, type <y>{}</>",
                     col_name, _type)
        replacements = {"int": "INTEGER", "str": "TEXT",
                        "bool": "INTEGER"}
        for before, after in replacements.items():
            _type = _type.replace(before, after)
        
        column_def.append(" ".join([col_name, _type]))
        logger.trace("Updated column definitions, column_def=<w>{}</>",
                     column_def)

    table_constraint = ["PRIMARY KEY(id)"]
    logger.trace("table_constraint = <w>{}</>", table_constraint)

    table_headers = ", ".join(column_def + table_constraint)
    await cur.execute(f"CREATE TABLE {module_name}({table_headers})")


async def save_record(file_name: str, module_name: str, headers: dict,
                      data: list) -> None:
    """Save any record to sqlite database"""
    logger.trace("Saving <w>{}</> into sqlite db <y>{}</>",
                 data, file_name)

    if not os.path.exists("output/"):
       os.makedirs("output/")

    con = await aiosqlite.connect(f"output/{file_name}",
                                  check_same_thread=False)
    cur = await con.cursor()

    # checking if table exists in python for optimisations
    if not await table_exists(cur, module_name):
        await create_table(cur, module_name, headers)

    qm = ", ".join(["?" for i in range(len(data)+1)])
    query = f"INSERT INTO {module_name} VALUES({qm})"
    logger.trace("Executing query = <w>{}</>", query)

    data_with_id = data.copy()
    data_with_id.insert(0, None)
    logger.trace("data_with_id = <w>{}</>", data_with_id)
    await cur.execute(query, data_with_id)

    logger.trace("Committing to db...")
    await con.commit()
