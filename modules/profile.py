"""Save info about profile of target user"""

import os
import time

from loguru import logger

from telethon.tl.functions.users import GetFullUserRequest

import modules.helpers.output as ot
import modules.helpers.temp as tp

logger = logger.opt(colors=True)


async def main(client, data, user: int):
    """Save info about user into output (basic profile data)"""
    logger.debug("Saving info about user (basic profile data), user=<y>{}</>",
                 user)
    u = await client.get_entity(user)
    full = await client(GetFullUserRequest(u))

    headers = {"time": "int", "user_id": "int", "username": "str",
               "phone_number": "str", "first_name": "str", "last_name": "str",
               "bio": "str", "is_premium": "bool", "is_close_friend": "bool",
               "lang_code": "str", "emoji_status": "int"}

    m_time = int(time.time())
    bio = full.full_user.about
    if u.emoji_status:
        logger.trace("User <y>{}</> has an emodji status", user)
        emoji_status = u.emoji_status.document_id
    else:
        logger.trace("User <y>{}</> doesn't have an emodji status", user)
        emoji_status = None

    results = [m_time, u.id, u.username, u.phone, u.first_name, u.last_name,
               bio, u.premium, u.close_friend, u.lang_code, emoji_status]
    logger.trace("Got results=<w>{}</>", results)

    prev_results = tp.get_prev_results("profile", str(u.id))

    if results[2:] != prev_results:
        await ot.save_record("profile", data["output"], headers, results)
        tp.save_results("profile", str(u.id), results[2:])
       
    else:
        logger.debug("New results the same as the previous, not saving")
