"""Start other modules automatically"""

from loguru import logger

import modules.helpers.errorhandle as eh

import modules.message as message
import modules.profile as profile
import modules.online as online
import modules.story as story

logger = logger.opt(colors=True)


async def start_static_trackers(client, data, timings) -> None:
    logger.trace("Starting static info trackers, timings=<y>{}</>...",
                 timings)

    for user_info in data["targets"]["users"]:
        if timings == "standart":
            await eh.log(client.loop.create_task(profile.main(client, data, user_info)))
            await eh.log(client.loop.create_task(story.main(client, data, user_info)))
        elif timings == "frequent":
            await eh.log(client.loop.create_task(online.main(client, data, user_info)))

async def start_message_handlers(client, data, event) -> None:
    logger.trace("Starting message handlers...")
    await eh.log(message.main(client, data, event))
