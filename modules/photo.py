"""Save info about target user's profile photo"""

import os
import time

from loguru import logger

import modules.output.output as ot
import modules.helpers.temp as tp

logger = logger.opt(colors=True)


async def main(client, user: int):
    """Save info about user's profile photo into output"""
    logger.debug("Saving info about user (photo), user=<y>{}</>",
                 user)
    u = await client.get_entity(user)

    headers = {"time": "int", "user_id": "int", "media_file": "str"}

    m_time = int(time.time())
    ns_time = int(time.time_ns())
    photos = [gen async for gen in client.iter_profile_photos(user)]
    logger.trace("Got user's <y>{}</> photos: <w>{}</> total",
                 user, len(photos))

    for photo in photos:
        photo_id = photo.id
        prev_results = tp.get_prev_results("photo", str(u.id))

        if prev_results is None or photo_id not in prev_results:
            file_path = f"output/photo/user{user}pfp{photo_id}"
            file = await client.download_media(photo,
                                               file=file_path)
            results = [m_time, u.id, file]
            logger.trace("Got results=<w>{}</>", results)

            await ot.save_record("photo", headers, results)
            tp.append_results("photo", str(u.id), photo_id)
           
        else:
            logger.debug("New results the same as the previous, not saving")

    if len(photos) == 0:
        logger.debug("No photos found for <y>{}</>, removing temp", user)
        tp.clear_temp("photo", str(u.id))
