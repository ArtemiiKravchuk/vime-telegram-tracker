"""Save info about online status of target user"""

import os
import time
import json

from loguru import logger

from telethon.tl.types import UserStatusOnline

import modules.helpers.output as ot
import modules.helpers.temp as tp

logger = logger.opt(colors=True)


async def main(client, data, user: int):
    """Save info about user's inline status into output"""
    logger.debug("Saving info about user (online status), user=<y>{}</>",
                 user)
    u = await client.get_entity(user)

    headers = {"time": "int", "user_id": "int", "status": "bool"}

    m_time = int(time.time())
    status = isinstance(u.status, UserStatusOnline)

    results = [m_time, u.id, status]
    logger.trace("Got results=<w>{}</>", results)

    prev_results = tp.get_prev_results("online", str(u.id))

    if results[2] != prev_results:
        await ot.save_record("online", data["output"], headers, results)
        tp.save_results("online", str(u.id), results[2])
       
    else:
        logger.debug("New results the same as the previous, not saving")
