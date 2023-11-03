"""Save info about target user's stories"""

import os
import time

from loguru import logger

from telethon.tl.functions.stories import GetUserStoriesRequest

import modules.helpers.output as ot
import modules.helpers.temp as tp

logger = logger.opt(colors=True)


async def main(client, data, user: int):
    """Save info about user's stories into output"""
    logger.debug("Saving info about user (stories), user=<y>{}</>",
                 user)
    u = await client.get_entity(user)

    headers = {"time": "int", "user_id": "int", "media_file": "str"}

    m_time = int(time.time())
    ns_time = int(time.time_ns())
    stories = await client(GetUserStoriesRequest(
        user_id=u.id
    ))
    logger.trace("Got user's <y>{}</> stories: <w>{}</>",
                 user, stories)

    for story in stories.stories.stories:
        story_id = story.id
        file = await client.download_media(story.media,
                                           file="output/media/")

        results = [m_time, u.id, file]
        logger.trace("Got results=<w>{}</>", results)

        prev_results = tp.get_prev_results("story", str(u.id))

        if prev_results is None or story_id not in prev_results:
            await ot.save_record("story", data["output"], headers, results)
            tp.append_results("story", str(u.id), story_id)
           
        else:
            logger.debug("New results the same as the previous, not saving")

    if len(stories.stories.stories) == 0:
        logger.debug("No stories found for <y>{}</>, removing temp", user)
        tp.clear_temp("story", str(u.id))
